# AKBS Package - File Index

## 📦 What You Have

This package contains 8 files totaling ~49KB. Here's what each one does:

---

## 🚀 START HERE

### **README.md** (8.4 KB)
**Your starting point - read this first!**

- Overview of the entire system
- Quick start guide (5 minutes)
- How it connects to your other projects
- Vision and next steps
- Example usage

---

## 💻 Core Code Files

### **akbs_ingest_markdown.py** (9.9 KB)
**The main ingestion pipeline**

What it does:
- Reads your Claude-processed markdown files
- Extracts metadata (chapter #, source, type)
- Chunks content intelligently (~1000 chars each)
- Extracts XML tags from AI-tagged files
- Generates embeddings automatically
- Stores everything in ChromaDB
- Provides query interface

Key classes/functions:
- `AKBSIngester` - Main class
- `ingest_file()` - Process single markdown file
- `ingest_directory()` - Process entire directory
- `query()` - Search the knowledge base
- `pretty_print_results()` - Display results nicely

### **akbs_query.py** (2.0 KB)
**Interactive query tool**

What it does:
- Command-line interface to your knowledge base
- Ask questions in natural language
- Get relevant answers from your documents

Usage:
```bash
# Interactive mode
python akbs_query.py

# Single query
python akbs_query.py "What is optimal pH for lettuce?"
```

### **requirements.txt** (216 bytes)
**Python dependencies**

Contains:
- `chromadb>=0.4.0` - Vector database
- `sentence-transformers>=2.2.0` - Embeddings

Install with:
```bash
pip install -r requirements.txt
```

### **test_akbs.py** (5.4 KB)
**Installation verification script**

What it tests:
1. Package installation (chromadb, sentence-transformers)
2. AKBS module import
3. Database creation
4. Sample file ingestion
5. Query functionality

Run with:
```bash
python test_akbs.py
```

---

## 📚 Documentation Files

### **AKBS_SETUP_GUIDE.md** (6.5 KB)
**Detailed setup and usage instructions**

Covers:
- Step-by-step installation
- File organization
- How ingestion works
- Usage examples (single file, directory, programmatic)
- Integration patterns (sensor system, teaching, simulation)
- File type detection
- Troubleshooting
- Performance notes

Read this for:
- Detailed explanations
- Advanced usage patterns
- Integration examples

### **AKBS_Project_Spec.md** (8.6 KB)
**Complete project specification and architecture**

Covers:
- Project overview and purpose
- Core capabilities
- Full architecture diagram
- Project structure
- Integration points for all systems
- Knowledge categories
- Implementation roadmap (Phases 1-4)
- Technical stack
- Success criteria

Read this for:
- Big picture understanding
- Long-term vision
- Architecture design
- Planning future features

### **QUICK_REFERENCE.md** (6.4 KB)
**Cheat sheet for common operations**

Quick lookup for:
- Installation commands
- Ingestion patterns
- Query examples
- Integration snippets
- Common queries to try
- Database management
- Troubleshooting
- File organization
- Tips & tricks

---

## 🎯 Usage Order (Recommended)

### Day 1: Setup & Verify
1. Read **README.md** (5 min)
2. Run `pip install -r requirements.txt`
3. Run **test_akbs.py** to verify installation
4. Skim **QUICK_REFERENCE.md** for commands

### Day 2: First Ingestion
1. Read **AKBS_SETUP_GUIDE.md** sections 1-3
2. Edit **akbs_ingest_markdown.py** with your paths
3. Run ingestion: `python akbs_ingest_markdown.py`
4. Test queries: `python akbs_query.py`

### Day 3: Integration
1. Read **AKBS_SETUP_GUIDE.md** integration section
2. Copy code to your sensor project
3. Start using in your system

### Later: Architecture & Planning
1. Read **AKBS_Project_Spec.md** fully
2. Plan your complete system architecture
3. Implement phases 2-4 as needed

---

## 📂 Where Files Will Be Used

```
Your Computer
├── This package (downloaded files)
│   ├── akbs_ingest_markdown.py ─────┐
│   ├── akbs_query.py                │
│   ├── requirements.txt              │
│   └── docs/ (all .md files)        │
│                                     │
├── Your markdown files               │
│   └── processed-chapters/           │
│                                     │
└── Generated files                   │
    └── data/                         │
        └── knowledge_db/ ←───────────┘
              (ChromaDB files)

Raspberry Pi (Future)
├── akbs_ingest_markdown.py (copied from above)
├── data/
│   └── knowledge_db/ (copied from above)
└── your-sensor-code.py (imports AKBSIngester)
```

---

## 🔄 Typical Workflow

1. **Process textbook with Claude** (your existing workflow)
   → Produces markdown files

2. **Ingest with this package**
   ```bash
   python akbs_ingest_markdown.py
   ```
   → Builds queryable knowledge base

3. **Query for information**
   ```bash
   python akbs_query.py
   ```
   → Get answers from your documents

4. **Integrate with sensor system** (future)
   ```python
   from akbs_ingest_markdown import AKBSIngester
   kb = AKBSIngester()
   guidance = kb.query("pH is 6.2, what should I do?")
   ```
   → Real-time decision support

---

## 💡 Quick Answers

**"Which file do I edit?"**
→ `akbs_ingest_markdown.py` (update paths in `main()` function)

**"How do I test it works?"**
→ Run `python test_akbs.py`

**"How do I use it?"**
→ See `QUICK_REFERENCE.md` for commands

**"What's the big picture?"**
→ Read `AKBS_Project_Spec.md`

**"How do I integrate it?"**
→ See integration section in `AKBS_SETUP_GUIDE.md`

**"I'm stuck, what do I read?"**
→ Check troubleshooting in `AKBS_SETUP_GUIDE.md`

---

## 🎓 Learning Path

**Beginner:**
- README.md
- test_akbs.py
- QUICK_REFERENCE.md

**Intermediate:**
- AKBS_SETUP_GUIDE.md
- Start using in projects

**Advanced:**
- AKBS_Project_Spec.md
- Build full integrated system

---

## 📊 File Size Reference

```
README.md                   8.4 KB  ████████
akbs_ingest_markdown.py     9.9 KB  █████████
akbs_query.py               2.0 KB  ██
requirements.txt            0.2 KB  
test_akbs.py                5.4 KB  █████
AKBS_SETUP_GUIDE.md         6.5 KB  ██████
AKBS_Project_Spec.md        8.6 KB  ████████
QUICK_REFERENCE.md          6.4 KB  ██████
                          ─────────
                          ~49 KB total
```

---

## ✅ Next Actions

1. [ ] Read README.md
2. [ ] Install dependencies: `pip install -r requirements.txt`
3. [ ] Test installation: `python test_akbs.py`
4. [ ] Put your markdown files in a directory
5. [ ] Edit `akbs_ingest_markdown.py` with your paths
6. [ ] Run ingestion
7. [ ] Query your knowledge base!

---

**Everything you need is here. Start with README.md and build from there!** 🚀
