import os
import xml.etree.ElementTree as ET

def validate_chunk(chunk_path):
    try:
        tree = ET.parse(chunk_path)
        root = tree.getroot()

        # Ensure the root tag is <mediawiki> and contains <page> elements
        if root.tag != "mediawiki":
            print(f"Error: Root element in {chunk_path} is not <mediawiki>")
            return False

        # Check if the chunk contains complete <page> tags
        pages = root.findall("page")
        if len(pages) == 0:
            print(f"Error: No <page> tags found in {chunk_path}")
            return False
        
        print(f"✅ {chunk_path} is valid with {len(pages)} pages.")
        return True

    except ET.ParseError as e:
        print(f"Error while parsing {chunk_path}: {e}")
        return False

def validate_chunks_in_directory(output_dir):
    chunk_files = [f for f in os.listdir(output_dir) if f.endswith('.xml')]
    
    # Validate each chunk file
    for chunk_file in chunk_files:
        chunk_path = os.path.join(output_dir, chunk_file)
        validate_chunk(chunk_path)

validate_chunks_in_directory('C:/Users/gowth/Documents/rag_datasets/wikidump/chunk_Folder')
