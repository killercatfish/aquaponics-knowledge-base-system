# AKBS Quick Reference Card

## Installation

```bash
pip install -r requirements.txt
```

## Test Installation

```bash
python test_akbs.py
```

---

## Ingestion

### Ingest Single File
```python
from pathlib import Path
from akbs_ingest_markdown import AKBSIngester

kb = AKBSIngester(db_path="./data/knowledge_db")
kb.ingest_file(
    Path("Chapter-01-Introduction.md"),
    source_name="RAS Textbook"
)
```

### Ingest Directory
```python
kb.ingest_directory(
    Path("./processed-chapters"),
    source_name="RAS Textbook"
)
```

### Ingest Multiple Directories
```python
# Chapters
kb.ingest_directory(
    Path("./2-Processed-Chapters"),
    source_name="RAS Book - Chapters"
)

# Topic guides
kb.ingest_directory(
    Path("./3-Topic-Guides"),
    source_name="RAS Book - Topics"
)
```

---

## Querying

### Interactive Query (Command Line)
```bash
python akbs_query.py
```

### Single Query (Command Line)
```bash
python akbs_query.py "What is optimal pH for lettuce?"
```

### Programmatic Query
```python
from akbs_ingest_markdown import AKBSIngester

kb = AKBSIngester(db_path="./data/knowledge_db")
results = kb.query("optimal pH for lettuce", n_results=5)

# Access results
for doc, meta in zip(results['documents'], results['metadatas']):
    print(f"Source: {meta['filename']}")
    print(f"Content: {doc}\n")
```

### Pretty Print Results
```python
results = kb.query("nitrogen cycle")
kb.pretty_print_results(results)
```

---

## Common Queries

```python
# Parameters
kb.query("optimal pH range for lettuce")
kb.query("temperature requirements for tilapia")
kb.query("dissolved oxygen levels for fish")

# Troubleshooting
kb.query("pH is 6.2, what should I do?")
kb.query("fish are gasping at surface")
kb.query("plants have yellow leaves")

# Learning
kb.query("explain nitrogen cycle")
kb.query("how does biofilter work")
kb.query("what is nitrification")

# System Design
kb.query("fish to plant ratio")
kb.query("pump size for 100 gallon system")
kb.query("grow bed depth")
```

---

## Integration Patterns

### With Sensor System
```python
from akbs_ingest_markdown import AKBSIngester

kb = AKBSIngester(db_path="/path/to/knowledge_db")

# Read sensor
current_ph = sensor.read_ph()
current_crop = "lettuce"

# Get guidance
results = kb.query(
    f"optimal pH for {current_crop}",
    n_results=3
)

if results['documents']:
    guidance = results['documents'][0]
    # Make decision based on guidance
```

### With Teaching Interface
```python
# Get lesson content
topic = "nitrogen cycle"
results = kb.query(f"explain {topic}", n_results=10)

lesson = {
    'topic': topic,
    'content': results['documents'],
    'sources': [m['filename'] for m in results['metadatas']]
}
```

### With Decision Making
```python
def should_adjust_ph(current_ph, target_ph, tolerance=0.5):
    """Check if pH adjustment needed"""
    
    # Query knowledge base for context
    guidance = kb.query(
        f"pH adjustment guidelines",
        n_results=3
    )
    
    # Make decision
    if abs(current_ph - target_ph) > tolerance:
        return True, guidance['documents'][0]
    return False, "pH is within acceptable range"
```

---

## Database Management

### Check Status
```python
kb = AKBSIngester(db_path="./data/knowledge_db")
print(f"Total documents: {kb.collection.count()}")
```

### List Metadata
```python
# Get all unique sources
results = kb.collection.get()
sources = set(m['source'] for m in results['metadatas'])
print(f"Sources: {sources}")
```

### Backup Database
```bash
# Database is in ./data/knowledge_db/
# Just copy the entire directory
cp -r ./data/knowledge_db ./backups/kb-backup-2025-10-29
```

### Move Database to Another Machine
```bash
# Copy to Raspberry Pi
scp -r ./data/knowledge_db pi@raspberrypi:/home/pi/aquaponics/data/
```

---

## File Organization

```
your-project/
├── akbs_ingest_markdown.py    # Main code
├── akbs_query.py               # Query tool
├── requirements.txt
├── data/
│   └── knowledge_db/          # Database (auto-created)
└── your-documents/
    ├── 2-Processed-Chapters/   # From Claude
    ├── 3-Topic-Guides/         # From Claude
    └── 4-Quick-References/     # From Claude
```

---

## Troubleshooting

### No Results Found
```python
# Try broader query
results = kb.query("pH")  # Instead of "exact pH value for specific plant"

# Check database has content
print(kb.collection.count())  # Should be > 0
```

### Slow First Query
```
First query loads ML models (10-30 seconds)
Subsequent queries are fast (<1 second)
This is normal!
```

### Import Error
```bash
pip install chromadb sentence-transformers
```

### Database Won't Persist
```python
# Make sure using PersistentClient
from chromadb import PersistentClient
client = PersistentClient(path="./data/knowledge_db")
```

---

## Tips & Tricks

### Best Query Practices
- ✓ Use natural language: "What is optimal pH for lettuce?"
- ✓ Be specific: "lettuce pH in NFT system"
- ✗ Avoid very generic: "pH" (too broad)
- ✓ Include context: "pH is 6.2, should I adjust?"

### Organizing Sources
```python
# Use descriptive source names
kb.ingest_directory(
    Path("./book1-chapters"),
    source_name="RAS Textbook v2 2023"
)

kb.ingest_directory(
    Path("./papers"),
    source_name="Research Papers - Lettuce"
)
```

### Performance
- Small chunks (500-1000 chars) = better precision
- Large chunks (1500-2000 chars) = more context
- Default 1000 is usually good

---

## Example Workflow

```python
from pathlib import Path
from akbs_ingest_markdown import AKBSIngester

# 1. Initialize
kb = AKBSIngester(db_path="./data/knowledge_db")

# 2. Ingest your processed documents
kb.ingest_directory(
    Path("./textbook/processed-chapters"),
    source_name="Aquaponics Bible 2024"
)

# 3. Query
results = kb.query("optimal pH for lettuce in NFT system")

# 4. Use results
for doc, meta in zip(results['documents'], results['metadatas']):
    print(f"\nFrom: {meta['filename']}")
    print(f"Chapter: {meta.get('chapter', 'N/A')}")
    print(f"Content:\n{doc[:300]}...")
```

---

## Quick Commands Reference

```bash
# Test installation
python test_akbs.py

# Ingest files (edit script first!)
python akbs_ingest_markdown.py

# Interactive query
python akbs_query.py

# Single query
python akbs_query.py "your question here"

# Install dependencies
pip install -r requirements.txt
```

---

**Keep this card handy while building your system!** 📋
