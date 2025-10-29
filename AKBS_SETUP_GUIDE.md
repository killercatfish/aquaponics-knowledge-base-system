# AKBS Markdown Ingestion - Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `chromadb` - Local vector database
- `sentence-transformers` - For generating embeddings

### 2. Organize Your Markdown Files

Place your Claude-processed markdown files in a directory structure like:

```
your-textbook/
├── 2-Processed-Chapters/
│   ├── Chapter-01-Introduction-Readable.md
│   ├── Chapter-01-Introduction-AI-Tagged.md
│   ├── Chapter-01-Introduction-Quick-Reference.md
│   ├── Chapter-02-System-Design-Readable.md
│   └── ...
└── 3-Topic-Guides/
    ├── Complete-Nutrients-Guide-Readable.md
    └── ...
```

### 3. Ingest Your Files

Edit `akbs_ingest_markdown.py` and update the `main()` function:

```python
def main():
    # Initialize ingester
    ingester = AKBSIngester(db_path="./data/knowledge_db")
    
    # Ingest your processed chapters
    ingester.ingest_directory(
        Path("./your-textbook/2-Processed-Chapters"),
        source_name="RAS Textbook"
    )
    
    # Ingest your topic guides
    ingester.ingest_directory(
        Path("./your-textbook/3-Topic-Guides"),
        source_name="RAS Textbook - Topic Guides"
    )
```

Then run:

```bash
python akbs_ingest_markdown.py
```

### 4. Query Your Knowledge Base

**Interactive mode:**
```bash
python akbs_query.py
```

**Single query from command line:**
```bash
python akbs_query.py "What is the optimal pH for lettuce?"
```

---

## How It Works

### Ingestion Pipeline

```
Markdown File
    ↓
Extract metadata (chapter #, type, source)
    ↓
Extract XML tags (if AI-tagged version)
    ↓
Chunk by headers and paragraphs (~1000 chars each)
    ↓
Generate embeddings automatically
    ↓
Store in ChromaDB with metadata
    ↓
Ready for querying!
```

### What Gets Stored

For each chunk:
- **Document text** - The actual content
- **Metadata:**
  - `filename` - Original file name
  - `chapter` - Chapter number (if detected)
  - `type` - readable, ai_tagged, or quick_reference
  - `source` - Name of source document
  - `has_tags` - XML tags found (for AI-tagged files)
  - `chunk_index` - Position in original document
  - `ingested_at` - When it was added

### Querying

When you query "What is optimal pH for lettuce?":
1. Your question is converted to an embedding
2. ChromaDB finds most similar document chunks
3. Returns top results with metadata
4. You see relevant content from your textbooks!

---

## Usage Examples

### Example 1: Ingest Single File

```python
from pathlib import Path
from akbs_ingest_markdown import AKBSIngester

ingester = AKBSIngester()
ingester.ingest_file(
    Path("Chapter-01-Introduction-Readable.md"),
    source_name="My Textbook"
)
```

### Example 2: Ingest Directory

```python
ingester.ingest_directory(
    Path("./processed-chapters"),
    source_name="Aquaponics Bible"
)
```

### Example 3: Query Programmatically

```python
# Query the knowledge base
results = ingester.query("optimal pH for lettuce", n_results=5)

# Access results
for doc, meta in zip(results['documents'], results['metadatas']):
    print(f"From: {meta['filename']}")
    print(f"Content: {doc[:200]}...")
    print()
```

### Example 4: Integration with Sensor System

```python
# In your sensor monitoring code
from akbs_ingest_markdown import AKBSIngester

kb = AKBSIngester()

# When pH reading comes in
current_ph = 6.2
current_crop = "lettuce"

# Query the knowledge base
results = kb.query(
    f"optimal pH range for {current_crop}",
    n_results=3
)

# Get guidance
if results['documents']:
    guidance = results['documents'][0]
    print(f"Knowledge Base says: {guidance}")
```

---

## File Types Handled

The ingester automatically detects file types:

- **`*-Readable.md`** → type: "readable"
- **`*-AI-Tagged.md`** → type: "ai_tagged" (extracts XML tags)
- **`*-Quick-Reference.md`** → type: "quick_reference"
- Other .md files → type: "general"

---

## Advanced Features

### Custom Chunk Size

```python
ingester = AKBSIngester()
chunks = ingester.chunk_markdown(text, max_chunk_size=500)  # Smaller chunks
```

### Extracting XML Tags

For AI-tagged files, tags are automatically extracted:

```python
xml_tags = ingester.extract_xml_tags(content)
# Returns: {'parameter': [...], 'value': [...], 'optimal': [...]}
```

### Check Knowledge Base Stats

```python
print(f"Total documents: {ingester.collection.count()}")
```

---

## Troubleshooting

### "Collection is empty"
- Make sure you've run the ingestion script first
- Check that your file paths are correct

### "No results found"
- Try broader queries
- Make sure relevant content was ingested
- Check that database path is correct

### "Permission denied" on database
- Make sure `./data/knowledge_db` directory is writable
- Try deleting and recreating the database

---

## Integration with Other Projects

### For Sensor System (Raspberry Pi)

Copy these files to your Pi:
```bash
scp akbs_ingest_markdown.py pi@raspberrypi:/home/pi/aquaponics/
scp requirements.txt pi@raspberrypi:/home/pi/aquaponics/
scp -r data/knowledge_db pi@raspberrypi:/home/pi/aquaponics/data/
```

Then in your sensor code:
```python
from akbs_ingest_markdown import AKBSIngester

kb = AKBSIngester(db_path="/home/pi/aquaponics/data/knowledge_db")
guidance = kb.query("pH is 6.2, what should I do?")
```

### For Teaching Interface

```python
# Get learning content
results = kb.query("explain nitrogen cycle", n_results=10)

# Extract readable content
lesson_content = "\n\n".join(results['documents'])
```

### For Simulation Platform

```python
# Get parameters for modeling
params = kb.query("tilapia growth rates at 75 degrees")
```

---

## Next Steps

1. ✅ Ingest your Claude-processed files
2. ✅ Test queries with `akbs_query.py`
3. Build Python API wrapper (optional)
4. Connect to sensor system
5. Add more documents over time

---

## Database Location

By default, the knowledge base is stored at:
```
./data/knowledge_db/
```

This directory contains:
- ChromaDB index files
- Embeddings
- Metadata

**Important:** This directory is PORTABLE! You can:
- Copy it to other machines
- Back it up
- Version control it (except it might be large)
- Share it with others

---

## Performance Notes

- First query may be slow (loading models)
- Subsequent queries are fast (<1 second)
- Ingestion speed: ~50-100 documents/minute
- Database size: ~10-50 MB per textbook (depending on size)

---

**You now have a queryable, persistent knowledge base from your Claude-processed textbooks!** 🎉
