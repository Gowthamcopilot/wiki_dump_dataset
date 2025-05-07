
# 📚 Wikipedia Dump Processing for LLM Pretraining

This repository contains a modular pipeline for transforming a raw 101GB Wikipedia XML dump into clean, structured plain text data suitable for training large language models (LLMs).

## 🗂️ Project Structure

```bash
.
├── chunk_wikidump.py               # Splits massive Wikipedia XML into manageable chunks
├── validate_chunks.py              # Validates structural integrity of each XML chunk
├── process_dataset.py             # Cleans and extracts data into structured format
├── sample_output.csv              # Example of the final processed dataset
└── README.md
```

---

## 🚀 Pipeline Overview

### 1. **Chunking (`chunk_wikidump.py`)**

Splits the massive Wikipedia dump into smaller XML files based on `<page>` tags to enable parallel processing and memory efficiency.

* Input: `enwiki-latest-pages-articles.xml`
* Output: `chunk_*.xml` files

### 2. **Validation (`validate_chunks.py`)**

Ensures that each chunk:

* Has valid opening and closing tags
* Contains well-formed XML
* Is safe for parsing by downstream scripts

### 3. **Dataset Creation (`process_dataset.py`)**

Processes each chunk to extract and clean article content. Produces a structured CSV with fields like:

* `ns`
* `id`
* `bytes`
* `title`
* `date`
* `categories`
* `entities`
* `plain_text` (cleaned, no templates/infoboxes/links)

Sample output is shown in `sample_output.csv`.

---

## 📦 Sample Output

| id    | title       | categories             | entities          | plain\_text                  |
| ----- | ----------- | ---------------------- | ----------------- | ---------------------------- |
| 12345 | Alan Turing | British mathematicians | Alan Turing, WWII | Alan Turing was a pioneer... |
| ...   | ...         | ...                    | ...               | ...                          |

---

## 🛠️ Requirements

* Python 3.8+
* `lxml`
* `regex`
* `pandas`
* `spacy`
* `dbpedia-spotlight` (optional, for concept linking)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ☁️ Cloud Usage

This pipeline is optimized for Google Cloud:

* Use `rclone` to upload/download chunked data
* Parallelize chunk processing across VMs for efficiency

---

## 📄 License

MIT License. See `LICENSE` for details.

---

Would you like me to generate the `requirements.txt` and example `sample_output.csv` based on assumed fields?
