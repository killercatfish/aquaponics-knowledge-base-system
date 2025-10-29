# AKBS Starter Package 🌱🧠

**Aquaponics Knowledge Base System - Markdown Ingestion Pipeline**

This package contains everything you need to turn your Claude-processed textbook markdown files into a queryable, persistent knowledge base.

---

## What You've Got

### Core Files

1. **`akbs_ingest_markdown.py`** - Main ingestion pipeline
   - Reads your markdown files
   - Chunks content intelligently
   - Extracts metadata and XML tags
   - Stores in ChromaDB with embeddings
   - Provides query interface

2. **`akbs_query.py`** - Interactive query tool
   - Command-line interface to your knowledge base
   - Ask questions in natural language
   - Get relevant answers from your textbooks

3. **`requirements.txt`** - Python dependencies
   - ChromaDB for vector storage
   - sentence-transformers for embeddings

4. **`AKBS_Project_Spec.md`** - Full project specification
   - Architecture overview
   - Integration points
   - Roadmap for full AKBS system

5. **`AKBS_SETUP_GUIDE.md`** - Detailed setup instructions
   - Step-by-step installation
   - Usage examples
   - Integration patterns

---

## Quick Start (5 Minutes)

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Setup Your Directory Structure

```bash
mkdir -p data/knowledge_db
mkdir -p processed-chapters
```

Put your Claude-processed markdown files in `processed-chapters/`

### 3. Edit `akbs_ingest_markdown.py`

Find the `main()` function and update paths:

```python
def main():
    ingester = AKBSIngester(db_path="./data/knowledge_db")
    
    # Update this path to your markdown files
    ingester.ingest_directory(
        Path("./processed-chapters"),
        source_name="Your Textbook Name"
    )
```

### 4. Ingest Your Files

```bash
python akbs_ingest_markdown.py
```

### 5. Query!

```bash
python akbs_query.py
```

Type questions like:
- "What is the optimal pH for lettuce?"
- "How do I manage dissolved oxygen?"
- "What temperature do tilapia need?"

---

## What This Connects To

```
Your Workflow                  AKBS System              Future Integration
─────────────────────────────────────────────────────────────────────────
Claude processes textbooks  →  This ingestion code  →  Sensor system
     ↓                              ↓                        ↓
Markdown + XML files       →  ChromaDB storage      →  Real-time queries
     ↓                              ↓                        ↓
Topic guides               →  Query interface       →  Decision making
```

---

## Your Complete Aquaponics Stack (Vision)

```
┌─────────────────────────────────────────────┐
│         Teaching Interface                  │ ← Future
│    (Guide learners through process)         │
├─────────────────────────────────────────────┤
│         Simulation Layer                    │ ← Future
│      (Digital twin testing)                 │
├─────────────────────────────────────────────┤
│    Knowledge Base (AKBS) ← YOU ARE HERE    │ ✓ NOW
│      (Query textbook knowledge)             │
├─────────────────────────────────────────────┤
│    Sensor System (Raspberry Pi)             │ ← In Progress
│      (Monitor & collect data)               │
├─────────────────────────────────────────────┤
│         Physical System                     │ ✓ EXISTS
│      (NFT hydroponics → aquaponics)        │
└─────────────────────────────────────────────┘
```

---

## How This Fits Your Workflow

### Current State:
1. ✅ You process textbooks with Claude
2. ✅ You get markdown files (readable + AI-tagged)
3. ✅ **NOW:** This code makes them queryable

### Next Steps:
1. Connect to your Raspberry Pi sensor system
2. When sensor reads pH = 6.2, query: "What does pH 6.2 mean for lettuce?"
3. Get guidance from your knowledge base
4. Make informed decisions automatically

---

## File Structure After Setup

```
your-akbs-project/
├── akbs_ingest_markdown.py    # Main ingestion code
├── akbs_query.py               # Query interface
├── requirements.txt            # Dependencies
├── AKBS_SETUP_GUIDE.md        # Detailed guide
├── AKBS_Project_Spec.md       # Full specification
├── data/
│   └── knowledge_db/          # ChromaDB storage (created on first run)
└── processed-chapters/         # Your markdown files go here
    ├── Chapter-01-*.md
    ├── Chapter-02-*.md
    └── ...
```

---

## Key Features

✅ **Local & Persistent** - Runs on your machine, survives restarts
✅ **Portable** - Copy the database to other machines
✅ **Fast** - Sub-second queries after initial load
✅ **Smart** - Uses embeddings for semantic search
✅ **Metadata-Rich** - Tracks chapters, sources, types
✅ **XML-Aware** - Extracts tags from AI-tagged files
✅ **Modular** - Easy to integrate with other projects

---

## Example Usage

### Ingest Files
```python
from pathlib import Path
from akbs_ingest_markdown import AKBSIngester

# Initialize
kb = AKBSIngester(db_path="./data/knowledge_db")

# Ingest a directory
kb.ingest_directory(
    Path("./processed-chapters"),
    source_name="RAS Textbook"
)
```

### Query Knowledge Base
```python
# Ask a question
results = kb.query("optimal pH for lettuce")

# Pretty print results
kb.pretty_print_results(results)
```

### Use in Sensor System
```python
# In your sensor monitoring code
current_ph = sensor.read_ph()
guidance = kb.query(f"pH is {current_ph}, what should I do?")
```

---

## What Makes This Special

This isn't just a document database. It's:

1. **Context-aware** - Understands relationships between concepts
2. **Source-tracked** - Knows where information came from
3. **Semantic** - Finds relevant content even with different wording
4. **Growing** - Add new documents anytime
5. **Integrated** - Designed to work with your other projects

---

## Next Steps After This Works

1. **Add More Documents**
   - Process more textbooks with Claude
   - Ingest research papers
   - Add your own operational learnings

2. **Build API Wrapper** (Optional)
   - REST API for other projects
   - FastAPI makes this easy

3. **Connect to Sensors**
   - Raspberry Pi queries knowledge base
   - Real-time decision support

4. **Expand to Simulation**
   - Use knowledge base for parameter validation
   - Inform simulation models

5. **Create Teaching Interface**
   - Query for learning content
   - Generate curriculum from knowledge base

---

## Troubleshooting

**Import Error: No module named 'chromadb'**
```bash
pip install chromadb sentence-transformers
```

**Database Won't Persist**
- Check that `./data/knowledge_db` is writable
- Make sure you're using `PersistentClient`, not `Client`

**No Results Found**
- Make sure you've ingested files first
- Try broader queries
- Check file paths in ingestion code

**Queries Are Slow**
- First query loads models (10-30 seconds)
- Subsequent queries are fast (<1 second)

---

## Contributing to This Project

As you use this system:
- Note what works well
- Track what needs improvement
- Add features you need
- Share learnings

**This is the foundation.** Everything else builds on this.

---

## The Vision

**Today:** You have textbook PDFs → Claude processes them → This makes them queryable

**Soon:** Sensors read data → Query knowledge base → Make informed decisions

**Future:** Complete autonomous aquaponics system with AI brain powered by your knowledge base

---

## Questions?

Read the full guides:
- **AKBS_SETUP_GUIDE.md** - Detailed usage instructions
- **AKBS_Project_Spec.md** - Complete system architecture

---

**You're building the brain. The sensors are the senses. Together, they think.** 🧠🌱

---

## License

Open source - build on it, share it, improve it.

---

**Start ingesting. Start querying. Start building.** 🚀
