# rust_docs_scraper.py - Rust Documentation Scraper
# A Multithreaded Rust / Web-Based HTML Documentation Scraper and Formatter
# v0.0.001 | (c) Ben Gorlick 2024 | github.com/bgorlick | 
# 
# MIT License with attribution and github link. Use at your own risk. This Software is provided as-is and is not guaranteed to work.
# The author is not responsible for any damages or losses incurred through the use of this software. 
# This tool is for educational purposes only and is not meant to be used for any malicious purposes.

# This software is designed to scrape Rust documentation for a given crate and version from the docs.rs website.
# It can handle multiple versions simultaneously and stores the extracted data in a SQLite database for further analysis.
# Additional functionalities include printing specific sections, saving raw HTML content, and extracting structural elements from the documentation.

# Example usage:
# python rust_docs_scraper.py regex --all --database --output rust_docs.txt -v -V 1.9.5
# Follow this command with something like this to query the database:
# sqlite3 rust_docs.db "SELECT url, stripped_html from sub_pages WHERE crate_name = 'regex' AND crate_version = '1.9.5' AND url = 'https://docs.rs/crate/regex/1.9.5/'"

# Other examples colud include (but may not work yet)
# python rust_docs_scraper.py tokio --modules --macros --verbose --output tokio_details.txt

# CLI Options:
# -m, --modules      Print module URLs.
# -a, --macros       Print macros and their descriptions.
# -s, --structs      Print structs and their descriptions.
# -e, --enums        Print enums and their descriptions.
# -f, --functions    Print functions and their descriptions.
# -t, --types        Print types and their descriptions.
# -d, --database     Save the collected data to a SQLite database.
# -v, --verbose      Print detailed descriptions.
# -V, --version      Specify the version(s) to fetch. Supports: latest, stable, ^VersionNumber, ~VersionNumber, VersionNumber..VersionNumber
# -l, --limit        Limit the number of items printed.
# -x, --filter       Filter items based on a regular expression pattern.
# -o, --output       Output the results to a file.
# -w, --workers      Maximum number of worker threads.
# --db-name          Specify the name of the SQLite database file.
# --db-path          Specify the path for the SQLite database file.
# --all              Print all available information.
# --details          Print the full HTML content of a specific item.

# You may need to install the following via pip:
# pip install requests beautifulsoup4 colorama html semver

import argparse
import concurrent.futures
import io
import logging
import os
import re
import time
import semver
import sqlite3
import html
from collections import defaultdict
from typing import DefaultDict, List, Optional, Tuple, Dict
from urllib.parse import urljoin

import colorama
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
from pip._vendor.idna import package_data

import traceback

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d')

# Global variables
BASE_URL = "https://docs.rs"
DEFAULT_DATABASE_FILE = "rust_docs.db"
DEFAULT_DATABASE_PATH = os.getcwd()

# Data structures
modules: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
macros: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
structs: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
enums: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
functions: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
types: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
sections: DefaultDict[str, DefaultDict[str, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
package_details: DefaultDict[str, DefaultDict[str, Dict[str, str]]] = defaultdict(lambda: defaultdict(dict))

# Initialize colorama
colorama.init()


def fetch_documentation(url: str, timeout=10) -> Optional[str]:
    """Fetches the documentation HTML for a given URL."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error("Failed to retrieve documentation for %s. Error: %s", url, e)
        return None


def is_sentence(line):
    # Check if the line has at least 5 words with 6 or more characters
    # Each word should only contain A-Za-z, commas, or periods
    matches = re.findall(r'\b[a-zA-Z,.]{6,}\b', line)
    return len(matches) >= 5


def wrap_text_to_80_chars(text):
    # Split text into individual lines
    lines = text.split('\n')
    wrapped_text = []
    current_paragraph = []

    for line in lines:
        # Check if the line is a sentence or is empty
        if not is_sentence(line) or not line.strip():
            # Process and add the accumulated paragraph text if it exists
            if current_paragraph:
                full_text = ' '.join(current_paragraph)
                while len(full_text) > 80:
                    last_space = full_text.rfind(' ', 0, 80)
                    if last_space == -1:  # No space found, add as is if it's less than 80 chars
                        break
                    wrapped_text.append(full_text[:last_space])
                    full_text = full_text[last_space + 1:]
                if full_text:
                    wrapped_text.append(full_text)
                current_paragraph = []
            wrapped_text.append(line)
        else:
            current_paragraph.append(line)

    # Ensure any remaining paragraph text is processed
    if current_paragraph:
        full_text = ' '.join(current_paragraph)
        while len(full_text) > 80:
            last_space = full_text.rfind(' ', 0, 80)
            if last_space == -1:
                break
            wrapped_text.append(full_text[:last_space])
            full_text = full_text[last_space + 1:]
        if full_text:
            wrapped_text.append(full_text)

    return '\n'.join(wrapped_text)


def strip_tags(html_content, preserve_structure=True):
    """
    Removes HTML tags from a string while preserving the structure if desired.

    If preserve_structure is True, it maintains indentation and line breaks.
    """

    # Decode HTML entities
    html_content = html.unescape(html_content)

    if preserve_structure:
        # Maintain structured elements like newlines and spaces in <pre> and <code>
        html_content = re.sub(r'<\s*br\s*/?>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<\s*pre[^>]*>', '\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<\s*/\s*pre>', '\n', html_content, flags=re.IGNORECASE)

        # Treat <code> blocks differently to preserve them
        code_blocks = re.findall(r'<code>(.*?)</code>', html_content, flags=re.DOTALL | re.IGNORECASE)
        placeholders = [f'{{CODE_BLOCK_{i}}}' for i in range(len(code_blocks))]
        for placeholder, code_block in zip(placeholders, code_blocks):
            html_content = html_content.replace(f'<code>{code_block}</code>', placeholder, 1)

        html_content = re.sub(r'<\s*p[^>]*>', '\n\n', html_content, flags=re.IGNORECASE)
        html_content = re.sub(r'<\s*/\s*p>', '\n\n', html_content, flags=re.IGNORECASE)

        # Remove all other HTML tags
        html_content = re.sub(r'<[^>]+>', '', html_content)

        # Clean up excessive whitespace and handle special formatting
        html_content = re.sub(r'\n{2,}', '\n\n', html_content)  # Normalize multiple newlines to double newlines
        html_content = re.sub(r'([\.!?])\s*\n+', r'\1\n', html_content)  # Correct newlines after punctuation
        html_content = re.sub(r'([\.!?])\s+', r'\1 ', html_content)  # Correct spacing after punctuation

        # Restore code blocks using placeholders
        for placeholder, code_block in zip(placeholders, code_blocks):
            html_content = html_content.replace(placeholder, code_block, 1)

        # Handle irregularities in sentences starting with "."
        html_content = re.sub(r'(?<=\.)(?=\s*[A-Z])', '. ', html_content)

        # Handle version numbers formatting
        html_content = re.sub(r'\n+\s*(\d+\.\d+\.\d+)\s*\n+', r'\n\1\n', html_content)
        
        # remove the second period from the end of sentences that have two periods like .. or ...
        html_content = re.sub(r'\.\.(\s+)', r'.\1', html_content)
        
        # If a sentence ends and a new sentence starts with only a single word on that line like this: End of a sentence. Word    -- we should move the "Word" to the next line
        html_content = re.sub(r'(\.\s)([A-Z][a-z]+)', r'\1\n\2', html_content)
        
        # Go through all lines where there are 3 newlines and remove the middle one
        html_content = re.sub(r'\n{3,}', r'\n\n', html_content)
        
        # Any line that starts with more than 12 spaces should be reduced to 4 spaces before the text starts
        html_content = re.sub(r'^\s{11,}', r'    ', html_content, flags=re.MULTILINE)
        
        # Handle isolated words like 'License' on a new line after a period
        html_content = re.sub(r'\.\s+([A-Z][a-z]+)\s*$', r'.\n\n\1', html_content, flags=re.MULTILINE)
        
        # Move "Usage:" to a new line if not at the beginning
        html_content = re.sub(r'(?<!\n)(Usage:)', r'\n\n\1', html_content)
        
        html_content = re.sub(r'(?<!\n)(For [Ee]xample:)', r'\n\n\1', html_content)

        # Correctly join isolated single words or short lines surrounded by blank lines
        html_content = re.sub(r'\n\n(?![Uu]sage:)([A-Z][a-z]+)\n\n', r' \1 ', html_content)
        
        # Correctly join isolated single words or short lines surrounded by blank lines
        html_content = re.sub(r'(?<=\.)\n\n([A-Z][a-z]+)\n', r' \1 ', html_content)
        
        # reduce to 80 characters
        html_content = wrap_text_to_80_chars(html_content)
        
        # any line where its just numbers with dots between them like 0.1.1 that has spaces before it should have the spaces removed but keep a new line between each number
        html_content = re.sub(r'^\s*(\d+\.\d+\.\d+)\s*$', r'\1', html_content, flags=re.MULTILINE)
        
    else:
        # Remove all HTML tags
        html_content = re.sub(r'<[^>]+>', '', html_content)

    return html_content.strip()


def parse_package_details(soup, crate_name, crate_version):
    package_details_container = soup.select_one('div.description-container')
    if package_details_container:
        crate_title = package_details_container.select_one('h1#crate-title').text.strip()
        crate_description = package_details_container.select_one('div.description').text.strip()
        logging.info(f"Found package details: {crate_title} - {crate_description}")
        package_details[crate_name][crate_version] = {
            'crate_title': crate_title,
            'crate_description': crate_description,
            'raw_html': str(package_details_container),
            'stripped_html': strip_tags(str(package_details_container), preserve_structure=True)
        }


def parse_modules(soup, crate_name, crate_version):
    module_containers = soup.select('div.item-name > a.mod')
    for module_container in module_containers:
        module_href = urljoin(BASE_URL, module_container.get('href'))
        module_name = module_container.text.strip()
        modules[crate_name][crate_version].append({
            'module_href': module_href,
            'module_name': module_name,
            'raw_html': str(module_container),
            'stripped_html': strip_tags(str(module_container), preserve_structure=True)
        })
        logging.info(f"Found module URL: {module_href}")


def parse_macros(soup, crate_name, crate_version):
    macro_containers = soup.select('div.item-name > a.macro')
    for macro_container in macro_containers:
        macro_name = macro_container.text.strip()
        macro_desc = macro_container.find_next('div', class_='desc').text.strip()
        macros[crate_name][crate_version].append({
            'macro_name': macro_name,
            'macro_desc': macro_desc,
            'raw_html': str(macro_container) + str(macro_container.find_next('div', class_='desc')),
            'stripped_html': strip_tags(str(macro_container) + str(macro_container.find_next('div', class_='desc')), preserve_structure=True)
        })
        logging.info(f"Found macro: {macro_name} - {macro_desc}")


def parse_documentation_sections(soup, crate_name, crate_version):
    for section in soup.select('h3'):
        title = section.text.strip()
        content = []
        raw_content = []
        next_sibling = section.next_sibling

        while next_sibling and next_sibling.name != 'h3':
            if next_sibling.name == 'p':
                content.append(next_sibling.text.strip())
                raw_content.append(str(next_sibling))
            elif next_sibling.name == 'pre':
                code_block = next_sibling.find('code')
                if code_block:
                    content.append(code_block.get_text(strip=True))
                    raw_content.append(str(next_sibling))
            next_sibling = next_sibling.next_sibling

        section_data = {
            'title': title,
            'content': '\n'.join(content),
            'raw_html': ''.join(raw_content),
            'stripped_html': strip_tags(''.join(raw_content), preserve_structure=True)
        }
        sections[crate_name][crate_version].append(section_data)
        logging.info(f"Found section: {title}")


def parse_structs(soup, crate_name, crate_version):
    struct_containers = soup.select('div.item-name > a.struct')
    for struct_container in struct_containers:
        struct_name = struct_container.text.strip()
        struct_desc = struct_container.find_next('div', class_='desc').text.strip()
        struct_data = {
            'struct_name': struct_name,
            'struct_desc': struct_desc,
            'raw_html': str(struct_container) + str(struct_container.find_next('div', class_='desc')),
            'stripped_html': strip_tags(str(struct_container) + str(struct_container.find_next('div', class_='desc')), preserve_structure=True)
        }
        structs[crate_name][crate_version].append(struct_data)
        logging.info(f"Found struct: {struct_name} - {struct_desc}")


def parse_enums(soup, crate_name, crate_version):
    enum_containers = soup.select('div.item-name > a.enum')
    for enum_container in enum_containers:
        enum_name = enum_container.text.strip()
        enum_desc = enum_container.find_next('div', class_='desc').text.strip()
        enum_data = {
            'enum_name': enum_name,
            'enum_desc': enum_desc,
            'raw_html': str(enum_container) + str(enum_container.find_next('div', class_='desc')),
            'stripped_html': strip_tags(str(enum_container) + str(enum_container.find_next('div', class_='desc')), preserve_structure=True)
        }
        enums[crate_name][crate_version].append(enum_data)
        logging.info(f"Found enum: {enum_name} - {enum_desc}")


def parse_functions(soup, crate_name, crate_version):
    function_containers = soup.select('div.item-name > a.fn')
    for function_container in function_containers:
        function_name = function_container.text.strip()
        function_desc = function_container.find_next('div', class_='desc').text.strip()
        function_data = {
            'function_name': function_name,
            'function_desc': function_desc,
            'raw_html': str(function_container) + str(function_container.find_next('div', class_='desc')),
            'stripped_html': strip_tags(str(function_container) + str(function_container.find_next('div', class_='desc')), preserve_structure=True)
        }
        functions[crate_name][crate_version].append(function_data)
        logging.info(f"Found function: {function_name} - {function_desc}")


def parse_types(soup, crate_name, crate_version):
    type_containers = soup.select('div.item-name > a.type')
    for type_container in type_containers:
        type_name = type_container.text.strip()
        type_desc = type_container.find_next('div', class_='desc').text.strip()
        type_data = {
            'type_name': type_name,
            'type_desc': type_desc,
            'raw_html': str(type_container) + str(type_container.find_next('div', class_='desc')),
            'stripped_html': strip_tags(str(type_container) + str(type_container.find_next('div', class_='desc')), preserve_structure=True)
        }
        types[crate_name][crate_version].append(type_data)
        logging.info(f"Found type: {type_name} - {type_desc}")


def parse_links(soup):
    link_containers = soup.select('a[href]')
    for link_container in link_containers:
        link_href = link_container.get('href')
        link_text = link_container.text.strip()
        logging.info(f"Found link: {link_text} - {link_href}")


def parse_documentation(html: str, url: str) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
    """Parses the HTML of a Rust crate documentation and stores details in data structures."""
    if not html:  # If raw_html_content is None, return early
        return None, None

    soup = BeautifulSoup(html, 'html.parser')
    stripped_html = strip_tags(str(soup), preserve_structure=True)

    # Extract crate name and version
    match = re.search(r'/crate/([^/]+)/([^/]+)', url)
    if match:
        crate_name, crate_version = match.groups()
        logging.info(f"Parsing documentation for crate '{crate_name}' version '{crate_version}'")
    else:
        # If the URL pattern doesn't match, skip parsing
        logging.warning(f"Unable to parse crate name and version from URL: {url}")
        return None, None

    parse_package_details(soup, crate_name, crate_version)
    parse_modules(soup, crate_name, crate_version)
    parse_macros(soup, crate_name, crate_version)
    parse_documentation_sections(soup, crate_name, crate_version)
    parse_structs(soup, crate_name, crate_version)
    parse_enums(soup, crate_name, crate_version)
    parse_functions(soup, crate_name, crate_version)
    parse_types(soup, crate_name, crate_version)
    parse_links(soup)

    return package_details[crate_name][crate_version], stripped_html


def save_sub_pages(c, sub_pages, crate_name, crate_version, raw_html_content=None, stripped_html=None, url=None):
    for sub_page_url in sub_pages:
        # Fetch the raw HTML content for the sub-page
        raw_html_content = fetch_documentation(sub_page_url)
        
        # Strip the HTML content to remove unnecessary elements
        stripped_html = strip_tags(raw_html_content, preserve_structure=True)
        
        c.execute("""INSERT OR REPLACE INTO sub_pages
                     (crate_name, crate_version, url, raw_html_content, stripped_html)
                        VALUES (?, ?, ?, ?, ?)""",
                    (crate_name, crate_version, sub_page_url, raw_html_content, stripped_html))
        logging.info(f"Inserted sub-page URL '{sub_page_url}' for crate '{crate_name}' version '{crate_version}' into the database")

        
# Database functions
def save_package_details(c, crate_name, crate_version, package_data):
    if package_data:
        crate_title = package_data.get('crate_title')
        crate_description = package_data.get('crate_description')
        raw_html = package_data.get('raw_html')
        stripped_html_pkg = package_data.get('stripped_html')

        c.execute("""INSERT OR REPLACE INTO package_details
                   (crate_name, crate_version, crate_title, crate_description, raw_html, stripped_html)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, crate_title, crate_description, raw_html, stripped_html_pkg))
        logging.info(f"Inserted package details for crate '{crate_name}' version '{crate_version}' into the database")
        

def save_raw_html_content(c, crate_name, crate_version, raw_html_content, url):
    if raw_html_content and url:
        c.execute("""INSERT OR REPLACE INTO raw_html_content
                     (crate_name, crate_version, raw_html_content)
                     VALUES (?, ?, ?)""",
                  (crate_name, crate_version, raw_html_content))
        logging.info(f"Inserted raw HTML content for crate '{crate_name}' version '{crate_version}' into the 'raw_html_content' table")


def save_stripped_html_content(c, crate_name, crate_version, stripped_html, url):
    if stripped_html and url:
        c.execute("""INSERT OR REPLACE INTO stripped_html_content
                     (crate_name, crate_version, stripped_html)
                     VALUES (?, ?, ?)""",
                  (crate_name, crate_version, stripped_html))
        logging.info(f"Inserted stripped HTML content for crate '{crate_name}' version '{crate_version}' into the 'stripped_html_content' table")


def save_documentation_sections(c, sections, crate_name, crate_version):
    section_data_list = sections.get(crate_name, {}).get(crate_version, [])
    for section_data in section_data_list:
        c.execute("""INSERT OR REPLACE INTO documentation_sections
                   (crate_name, crate_version, section_title, section_content, raw_html, stripped_html)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, section_data['title'], section_data['content'],
                   section_data['raw_html'], section_data['stripped_html']))
        logging.info(f"Inserted section '{section_data['title']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_modules(c, modules, crate_name, crate_version):
    module_data_list = modules.get(crate_name, {}).get(crate_version, [])
    for module_data in module_data_list:
        c.execute("""INSERT OR REPLACE INTO modules
                   (crate_name, crate_version, module_href, module_name, raw_html, stripped_html)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, module_data['module_href'], module_data['module_name'],
                   module_data['raw_html'], module_data['stripped_html']))
        logging.info(f"Inserted module '{module_data['module_name']}' with URL '{module_data['module_href']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_macros(c, macros, crate_name, crate_version):
    macro_data_list = macros.get(crate_name, {}).get(crate_version, [])
    for macro_data in macro_data_list:
        c.execute("""INSERT OR REPLACE INTO macros
                   (crate_name, crate_version, macro_name, macro_desc, raw_html, stripped_html)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, macro_data['macro_name'], macro_data['macro_desc'],
                   macro_data['raw_html'], macro_data['stripped_html']))
        logging.info(f"Inserted macro '{macro_data['macro_name']}' with description '{macro_data['macro_desc']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_structs(c, structs, crate_name, crate_version):
    struct_data_list = structs.get(crate_name, {}).get(crate_version, [])
    for struct_data in struct_data_list:
        c.execute("""INSERT OR REPLACE INTO structs
                   (crate_name, crate_version, struct_name, struct_desc, raw_html, stripped_html)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, struct_data['struct_name'], struct_data['struct_desc'],
                   struct_data['raw_html'], struct_data['stripped_html']))
        logging.info(f"Inserted struct '{struct_data['struct_name']}' with description '{struct_data['struct_desc']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_enums(c, enums, crate_name, crate_version):
    enum_data_list = enums.get(crate_name, {}).get(crate_version, [])
    for enum_data in enum_data_list:
        c.execute("""INSERT OR REPLACE INTO enums
                    (crate_name, crate_version, enum_name, enum_desc, raw_html, stripped_html)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, enum_data['enum_name'], enum_data['enum_desc'],
                   enum_data['raw_html'], enum_data['stripped_html']))
        logging.info(f"Inserted enum '{enum_data['enum_name']}' with description '{enum_data['enum_desc']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_functions(c, functions, crate_name, crate_version):
    function_data_list = functions.get(crate_name, {}).get(crate_version, [])
    for function_data in function_data_list:
        c.execute("""INSERT OR REPLACE INTO functions
                    (crate_name, crate_version, function_name, function_desc, raw_html, stripped_html)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, function_data['function_name'], function_data['function_desc'],
                   function_data['raw_html'], function_data['stripped_html']))
        logging.info(f"Inserted function '{function_data['function_name']}' with description '{function_data['function_desc']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_types(c, types, crate_name, crate_version):
    type_data_list = types.get(crate_name, {}).get(crate_version, [])
    for type_data in type_data_list:
        c.execute("""INSERT OR REPLACE INTO types
                    (crate_name, crate_version, type_name, type_desc, raw_html, stripped_html)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                  (crate_name, crate_version, type_data['type_name'], type_data['type_desc'],
                   type_data['raw_html'], type_data['stripped_html']))
        logging.info(f"Inserted type '{type_data['type_name']}' with description '{type_data['type_desc']}' for crate '{crate_name}' version '{crate_version}' into the database")


def save_to_database(db_path, db_name, url=None, package_data=None, stripped_html=None, raw_html=None, sub_pages=None):
    """Saves the collected data to a SQLite database."""
    
    logging.info("[save_to_database] Args: db_path=%s, db_name=%s, url=%s, package_data=%s, stripped_html=%s", db_path, db_name, url, package_data, stripped_html)
    # wait 2 seconds before starting
    time.sleep(3)
    db_file = os.path.join(db_path, db_name)
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS package_details
                 (crate_name TEXT, crate_version TEXT, crate_title TEXT, crate_description TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version))''')
    c.execute('''CREATE TABLE IF NOT EXISTS documentation_sections
                 (crate_name TEXT, crate_version TEXT, section_title TEXT, section_content TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, section_title))''')
    c.execute('''CREATE TABLE IF NOT EXISTS modules
                 (crate_name TEXT, crate_version TEXT, module_href TEXT, module_name TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, module_href))''')
    c.execute('''CREATE TABLE IF NOT EXISTS macros
                 (crate_name TEXT, crate_version TEXT, macro_name TEXT, macro_desc TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, macro_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS structs
                 (crate_name TEXT, crate_version TEXT, struct_name TEXT, struct_desc TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, struct_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS enums
                 (crate_name TEXT, crate_version TEXT, enum_name TEXT, enum_desc TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, enum_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS functions
                 (crate_name TEXT, crate_version TEXT, function_name TEXT, function_desc TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, function_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS types
                 (crate_name TEXT, crate_version TEXT, type_name TEXT, type_desc TEXT, raw_html TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, type_name))''')
    c.execute('''CREATE TABLE IF NOT EXISTS raw_html_content
             (crate_name TEXT, crate_version TEXT, raw_html_content TEXT, PRIMARY KEY (crate_name, crate_version))''')
    c.execute('''CREATE TABLE IF NOT EXISTS stripped_html_content
                    (crate_name TEXT, crate_version TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version))''')
    c.execute('''CREATE TABLE IF NOT EXISTS sub_pages
                    (crate_name TEXT, crate_version TEXT, url TEXT, raw_html_content TEXT, stripped_html TEXT, PRIMARY KEY (crate_name, crate_version, url))''')

    # Save data to the database
    crate_name, crate_version = None, None
    if url:
        match = re.search(r'/crate/([^/]+)/([^/]+)', url)
        if match:
            crate_name, crate_version = match.groups()
        else:
            logging.warning(f"Unable to extract crate name and version from URL: {url}")

    if crate_name and crate_version:
        save_package_details(c, crate_name, crate_version, package_data)
        save_raw_html_content(c, crate_name, crate_version, raw_html, url)  
        save_stripped_html_content(c, crate_name, crate_version, stripped_html, url)
        save_sub_pages(c, sub_pages, crate_name, crate_version, raw_html, stripped_html, url)
        save_documentation_sections(c, sections, crate_name, crate_version)
        save_modules(c, modules, crate_name, crate_version)
        save_macros(c, macros, crate_name, crate_version)
        save_structs(c, structs, crate_name, crate_version)
        save_enums(c, enums, crate_name, crate_version)
        save_functions(c, functions, crate_name, crate_version)
        save_types(c, types, crate_name, crate_version)

    logging.info("Committing changes to the database")
    conn.commit()
    conn.close()


def print_documentation(local_args):
    """Prints the collected documentation based on the provided command-line arguments."""
    output_buffer = io.StringIO()
    for crate_name, version_data in modules.items():
        for crate_version, module_urls in version_data.items():
            if local_args.modules:
                output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                for module_url in module_urls:
                    output_buffer.write(f"{Fore.BLUE}  Module URL: {module_url}{Style.RESET_ALL}\n")

            if local_args.macros:
                output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                for macro_name, macro_desc in macros[crate_name][crate_version]:
                    output_buffer.write(f"{Fore.CYAN}  Macro: {macro_name}{Style.RESET_ALL}\n")
                    if local_args.verbose:
                        output_buffer.write(f"{Fore.YELLOW}    Description: {macro_desc}{Style.RESET_ALL}\n")

            if local_args.structs:
                output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                for struct_name, struct_desc in structs[crate_name][crate_version]:
                    output_buffer.write(f"{Fore.CYAN}  Struct: {struct_name}{Style.RESET_ALL}\n")
                    if local_args.verbose:
                        output_buffer.write(f"{Fore.YELLOW}    Description: {struct_desc}{Style.RESET_ALL}\n")

            if local_args.enums:
                output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                for enum_name, enum_desc in enums[crate_name][crate_version]:
                    output_buffer.write(f"{Fore.CYAN}  Enum: {enum_name}{Style.RESET_ALL}\n")
                    if local_args.verbose:
                        output_buffer.write(f"{Fore.YELLOW}    Description: {enum_desc}{Style.RESET_ALL}\n")

            if local_args.functions:
                output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                for function_name, function_desc in functions[crate_name][crate_version]:
                    output_buffer.write(f"{Fore.CYAN}  Function: {function_name}{Style.RESET_ALL}\n")
                    if local_args.verbose:
                        output_buffer.write(f"{Fore.YELLOW}    Description: {function_desc}{Style.RESET_ALL}\n")

            if local_args.types:
                output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                for type_name, type_desc in types[crate_name][crate_version]:
                    output_buffer.write(f"{Fore.CYAN}  Type: {type_name}{Style.RESET_ALL}\n")
                    if local_args.verbose:
                        output_buffer.write(f"{Fore.YELLOW}    Description: {type_desc}{Style.RESET_ALL}\n")

            if local_args.details:
                for item_type, item_data in [
                    ("Module", module_urls),
                    ("Macro", macros[crate_name][crate_version]),
                    ("Struct", structs[crate_name][crate_version]),
                    ("Enum", enums[crate_name][crate_version]),
                    ("Function", functions[crate_name][crate_version]),
                    ("Type", types[crate_name][crate_version]),
                ]:
                    if local_args.filter:
                        item_data = [item for item in item_data if re.search(local_args.filter, str(item))]

                    for item in item_data[:local_args.limit]:
                        if item_type == "Module":
                            item_url = item
                            output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                            output_buffer.write(f"{Fore.BLUE}  {item_type} URL: {item_url}{Style.RESET_ALL}\n")
                            raw_html_content = fetch_documentation(item_url)
                            if raw_html_content:
                                output_buffer.write(f"{Fore.YELLOW}{raw_html_content}{Style.RESET_ALL}\n")
                        else:
                            item_name, item_desc = item
                            output_buffer.write(f"{Fore.GREEN}Crate: {crate_name} (Version: {crate_version}){Style.RESET_ALL}\n")
                            output_buffer.write(f"{Fore.CYAN}  {item_type}: {item_name}{Style.RESET_ALL}\n")
                            output_buffer.write(f"{Fore.YELLOW}    Description: {item_desc}{Style.RESET_ALL}\n")

    if local_args.output:
        with open(local_args.output, "w", encoding="utf-8") as file:
            file.write(output_buffer.getvalue())
    else:
        print(output_buffer.getvalue())


def crawl_crate(crate_name: str, version: Optional[str]=None, max_workers: int=10) -> None:
    """Crawls the documentation for a given Rust crate."""
    if version is None:
        logging.info(f"No version specified, fetching the latest version for crate '{crate_name}'")
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/latest"]
        version_filter = None
    elif version == "latest":
        logging.info(f"Fetching the latest version for crate '{crate_name}'")
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/latest"]
        version_filter = None
    elif version == "stable":
        logging.info(f"Fetching the stable version for crate '{crate_name}'")
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/stable"]
        version_filter = None
    elif version.startswith("^"):
        major_version = semver.parse_version_info(version[1:]).major
        logging.info(f"Fetching the latest version in the {major_version}.x.x range for crate '{crate_name}'")
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/{major_version}"]
        version_filter = re.compile(rf"^{BASE_URL}/crate/{crate_name}/{major_version}\.\d+\.\d+")
    elif version.startswith("~"):
        major_minor_version = re.match(r"~(\d+\.\d+)", version).group(1)
        logging.info(f"Fetching the latest version in the {major_minor_version}.x range for crate '{crate_name}'")
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/{major_minor_version}"]
        version_filter = re.compile(rf"^{BASE_URL}/crate/{crate_name}/{major_minor_version}\.\d+")
    elif ".." in version:
        start_version, end_version = version.split("..")
        start_version_info = semver.parse_version_info(start_version)
        end_version_info = semver.parse_version_info(end_version)
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/{version_str}" for version_str in semver.range(start_version_info, end_version_info)]
        logging.info(f"Fetching versions between {start_version} and {end_version} (inclusive) for crate '{crate_name}'")
        version_filter = re.compile(rf"^{BASE_URL}/crate/{crate_name}/({'|'.join([re.escape(v) for v in semver.range(start_version_info, end_version_info)])})")
    else:
        logging.info(f"Fetching version {version} for crate '{crate_name}'")
        urls_to_visit = [f"{BASE_URL}/crate/{crate_name}/{version}"]
        version_filter = re.compile(rf"^{BASE_URL}/crate/{crate_name}/{re.escape(version)}")

    visited_urls = set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        logging.info(f"Created ThreadPoolExecutor with {max_workers} workers")

        while urls_to_visit:
            url = urls_to_visit.pop(0)
            visited_urls.add(url)
            logging.info(f"Fetching documentation for URL: {url}")

            raw_html_content = fetch_documentation(url)

            if raw_html_content:
                logging.info(f"Successfully fetched documentation for URL: {url}")

                # Get the package details for the current crate and version
                package_data, stripped_html = parse_documentation(raw_html_content, url)
                logging.info(f"Parsed package details: {package_data} {url}")
                logging.debug(f"Passing {url} content here: {stripped_html} to the parse_documentation function")
                
                soup = BeautifulSoup(raw_html_content, 'html.parser')
                new_urls = [urljoin(BASE_URL, link.get('href')) for link in soup.select('a[href^="/"]')]
                if version_filter:
                    new_urls = [url for url in new_urls if version_filter.match(url)]
                new_urls = [url for url in new_urls if url not in visited_urls]
                logging.info(f"Found {len(new_urls)} new URLs to visit")

                # Save the data to the database, including the sub-pages (new_urls)
                save_to_database(DEFAULT_DATABASE_PATH, DEFAULT_DATABASE_FILE, url, package_data, stripped_html, raw_html_content, new_urls)

                for new_url in new_urls:
                    if new_url not in urls_to_visit:
                        urls_to_visit.append(new_url)
                        logging.info(f"Added URL to visit: {new_url}")

                executor.map(fetch_documentation, urls_to_visit)
                logging.info(f"Submitted {len(urls_to_visit)} URLs to the executor")
            else:
                logging.warning(f"Failed to fetch documentation for URL: {url}")


def main():
    parser = argparse.ArgumentParser(description="Crawl and parse Rust crate documentation.")
    parser.add_argument("crate_name", help="The name of the Rust crate.")
    parser.add_argument("-m", "--modules", action="store_true", help="Print module URLs.")
    parser.add_argument("-a", "--macros", action="store_true", help="Print macros and their descriptions.")
    parser.add_argument("-s", "--structs", action="store_true", help="Print structs and their descriptions.")
    parser.add_argument("-e", "--enums", action="store_true", help="Print enums and their descriptions.")
    parser.add_argument("-f", "--functions", action="store_true", help="Print functions and their descriptions.")
    parser.add_argument("-t", "--types", action="store_true", help="Print types and their descriptions.")
    parser.add_argument("-d", "--database", action="store_true", help="Save the collected data to a SQLite database.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed descriptions.")
    parser.add_argument("-V", "--version", help="Specify the version(s) to fetch. Supports: latest, stable, ^VersionNumber, ~VersionNumber, VersionNumber..VersionNumber")
    parser.add_argument("-l", "--limit", type=int, default=0, help="Limit the number of items printed.")
    parser.add_argument("-x", "--filter", help="Filter items based on a regular expression pattern.")
    parser.add_argument("-o", "--output", help="Output the results to a file.")
    parser.add_argument("-w", "--workers", type=int, default=10, help="Maximum number of worker threads.")
    parser.add_argument("--db-name", default=DEFAULT_DATABASE_FILE, help="Specify the name of the SQLite database file.")
    parser.add_argument("--db-path", default=DEFAULT_DATABASE_PATH, help="Specify the path for the SQLite database file.")
    parser.add_argument("--all", action="store_true", help="Print all available information.")
    parser.add_argument("--details", action="store_true", help="Print the full HTML content of a specific item.")

    args = parser.parse_args()

    try:
        crawl_crate(args.crate_name, version=args.version, max_workers=args.workers)

        if args.database:
            save_to_database(args.db_path, args.db_name)

        if args.all or any([args.modules, args.macros, args.structs, args.enums, args.functions, args.types, args.details]):
            print_documentation(args)
        else:
            print("No output option selected. Use -h or --help to see available options.")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")
    except Exception as e:
        logging.error(f"An error occurred: {e}\n{traceback.format_exc()}")
        raise
    finally:
        colorama.deinit()
        logging.info("Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
