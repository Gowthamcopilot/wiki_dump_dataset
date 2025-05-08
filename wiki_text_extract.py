import xml.etree.ElementTree as ET
import mwparserfromhell
import pandas as pd
import re
from tqdm import tqdm
import time
import json


with open("file_list.json", "r") as f:
    url_list = json.load(f)

HEADERS_TO_REMOVE = [
    "See also", "References", "External links", "Further reading", "Notes", "Sources"
]

def extract_metadata(wikicode):
    """Extract categories and unique entities from wikicode."""
    categories = []
    entities = []

    for node in wikicode.nodes:
        if isinstance(node, mwparserfromhell.nodes.Wikilink):
            title = str(node.title).strip()
            if title.startswith("Category:"):
                categories.append(str(title[9:]))
            elif not title.startswith(("File:", "Image:")):
                entity = node.text or node.title
                if entity:
                    entities.append(str(entity))  # Store the entity as is, no str conversion here

    return categories, entities

def clean_wikicode(wikicode):
    """Remove non-article content like image/file links and formatting templates."""
    clean_nodes = []

    for node in wikicode.nodes:
        if isinstance(node, mwparserfromhell.nodes.Wikilink):
            title = str(node.title).strip()
            if title.startswith(("File:", "Image:", "Category:")):
                continue

        elif isinstance(node, mwparserfromhell.nodes.Template):
            if any(keyword in str(node).lower() for keyword in ['thumb', 'right', 'left', 'upright', 'px']):
                continue

        clean_nodes.append(node)

    cleaned = mwparserfromhell.wikicode.Wikicode(clean_nodes)
    return str(cleaned.strip_code())

def remove_postarticle_section(text, headers):
    """Remove sections after headers like References or External links."""
    pattern = r"(?i)==+\s*(" + "|".join(re.escape(h) for h in headers) + r")\s*==+.*"
    match = re.search(pattern, str(text))
    if match:
        return text[:match.start()].strip()
    return text.strip()

def remove_tables(text):
    """Remove all wikitext tables."""
    return re.sub(r"\{\|[\s\S]*?\|\}", "", text)

# Main processing
data = []
i = 0
for url in url_list:
    start_time = time.time()
    tree = ET.parse(url)
    root = tree.getroot()
    pages = root.findall('.//page')

    for page in tqdm(pages, desc=f"Processing chunk_{url[60:]}", unit="page"):
        ns = page.find('ns').text
        if ns == '0':
            bytes_ = int(page.find('revision/text').attrib.get('bytes', 0))
            if bytes_ > 1000:
                id_ = page.find('id').text
                title = page.find('title').text
                text = page.find('revision/text').text
                date = page.find('revision/timestamp').text[:10]

                # Extract categories from full text before trimming
                full_wikicode = mwparserfromhell.parse(text or "")
                categories, entities = extract_metadata(full_wikicode)

                # Clean and extract entities from trimmed text
                text_clean = remove_postarticle_section(text, HEADERS_TO_REMOVE)
                text_clean = remove_tables(text_clean)
                wikicode = mwparserfromhell.parse(text_clean)

                plain_text = clean_wikicode(wikicode)

                data.append({
                    'id': id_,
                    'bytes': bytes_,
                    'title': title,
                    'text': plain_text,
                    'date': date,
                    'categories': categories,
                    'entities': entities
                })
    file_processed = url_list.pop(0)           
    i = i + 1
    end_time = time.time()
    print(f"Chunk {file_processed} processed in {end_time - start_time:.2f} seconds")
    if i % 30 == 0:
        con = input("do you want to continue to next batch : ")
        if con.lower() == "n":
            break

df = pd.DataFrame(data)
df.to_parquet('clean_wiki_test_02.parquet', engine='pyarrow')
print("------------- Saved successfully -----------")

with open("file_list.json", "w") as f:
    json.dump(url_list, f)




