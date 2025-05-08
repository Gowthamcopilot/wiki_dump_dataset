
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

| id    | title       | plain_text             | cetegories        | entities                     | date        |
| ----- | ----------- | ---------------------- | ----------------- | ---------------------------- |-------------|
| 12345 | Alan Turing | British mathematicians | Alan Turing, WWII | Alan Turing was a pioneer... |12-02-2018   |
| ...   | ...         | ...                    | ...               | ...                          |

---

## 🛠️ Requirements

* Python 3.8+
* `lxml`
* `regex`
* `pandas`
* `spacy`
* `mwparserfromhell`
* `xml`

##🚀 Applications and Use Cases
This dataset is a cleaned and enriched version of the Wikipedia dump, optimized for NLP model training and semantic analysis. It can power a wide range of AI, research, and educational projects.

🔬 NLP Research & Model Training
Train language models (GPT-style, BERT-style) on high-quality, plain text from Wikipedia.

Fine-tune existing models for downstream tasks like summarization or question answering.

🧠 Knowledge Graph Construction
Extract entities, categories, and concepts to build custom knowledge graphs.

Useful for semantic search, recommendation engines, or domain-specific ontologies.

🎓 Education & Prototyping
Great for students and educators to experiment with LLMs and document parsing.


🔍 Semantic Search and Retrieval
Index the plain-text content with vector databases for use in retrieval-augmented generation (RAG) pipelines.



## 📄 License

MIT License. See `LICENSE` for details.

