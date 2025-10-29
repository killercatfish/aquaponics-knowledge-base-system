# Aquaponics Knowledge Base System (AKBS)

## Project Overview

A local, persistent knowledge management system that serves as the "brain" for intelligent aquaponics decision-making. This system extracts, stores, and retrieves domain knowledge from scientific papers, textbooks, and operational data to inform automated system decisions.

---

## Purpose

**Problem:** Aquaponics requires deep domain knowledge (biology, chemistry, engineering) to operate successfully. Sensors produce data, but without context, the numbers are meaningless.

**Solution:** Build a queryable knowledge base that:
- Stores aquaponics domain knowledge locally
- Provides context for sensor readings
- Enables AI-driven decision making
- Grows with system experience
- Integrates with multiple projects

---

## Core Capabilities

### 1. **Knowledge Ingestion**
- Extract text from PDFs (research papers, textbooks, manuals)
- Parse and chunk content into semantic sections
- Generate embeddings for vector search
- Store with metadata (source, page, topic, date)

### 2. **Persistent Storage**
- Local vector database (ChromaDB)
- Survives system restarts
- Portable across machines
- Versioned knowledge snapshots

### 3. **Intelligent Retrieval**
- Natural language queries
- Context-aware search
- Ranked relevance
- Source attribution

### 4. **Growth & Learning**
- Add new documents over time
- Integrate operational learnings
- Version control for knowledge updates
- Export/import capabilities

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                  AKBS Core System                     │
├──────────────────────────────────────────────────────┤
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Ingestion │  │   Storage    │  │  Retrieval │ │
│  │   Pipeline  │→ │  (ChromaDB)  │ ← │  Interface │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│         ↑                                     ↓      │
└─────────┼─────────────────────────────────────┼─────┘
          │                                     │
    PDF/Text Input                         Query API
          │                                     │
     ┌────┴─────────────────────────────────────┴────┐
     │          Integration Layer (REST/Python)      │
     └────┬─────────────┬──────────────┬────────────┘
          ↓             ↓              ↓
   ┌──────────┐  ┌──────────┐  ┌─────────────┐
   │  Sensor  │  │ Teaching │  │ Simulation  │
   │  System  │  │Interface │  │  Platform   │
   └──────────┘  └──────────┘  └─────────────┘
```

---

## Project Structure

```
aquaponics-knowledge-base/
├── README.md
├── requirements.txt
├── config/
│   └── settings.yaml           # Database paths, model configs
├── data/
│   ├── raw/                    # Original PDFs
│   ├── processed/              # Extracted text chunks
│   └── knowledge_db/           # ChromaDB persistent storage
├── src/
│   ├── ingestion/
│   │   ├── pdf_extractor.py   # Extract text from PDFs
│   │   ├── chunker.py          # Split into semantic chunks
│   │   └── embedder.py         # Generate embeddings
│   ├── storage/
│   │   ├── db_manager.py       # ChromaDB operations
│   │   └── schema.py           # Data models
│   ├── retrieval/
│   │   ├── query_engine.py     # Search interface
│   │   └── ranker.py           # Result ranking
│   └── api/
│       └── knowledge_api.py    # REST/Python interface
├── tests/
└── examples/
    └── example_queries.py
```

---

## Integration Points

### For Sensor System (Raspberry Pi)
```python
from akbs import KnowledgeBase

kb = KnowledgeBase()

# Query optimal ranges
result = kb.query("optimal pH range for lettuce in NFT system")

# Get troubleshooting guidance
guidance = kb.query(f"pH is {current_ph}, what should I do?")
```

### For Teaching Interface
```python
# Retrieve learning content
lesson = kb.get_topic("nitrogen cycle in aquaponics", 
                      difficulty="beginner")

# Get definitions
definition = kb.query("what is nitrification?")
```

### For Simulation Platform
```python
# Get system parameters for modeling
params = kb.get_parameters("tilapia growth rates at 75°F")
```

---

## Knowledge Categories

1. **Biological Knowledge**
   - Fish species requirements (temp, pH, DO, feeding)
   - Plant growth parameters (nutrients, light, pH)
   - Bacterial processes (nitrification, biofilter cycling)

2. **Chemical Knowledge**
   - Water chemistry (pH, ammonia, nitrites, nitrates)
   - Nutrient profiles and deficiencies
   - Treatment protocols

3. **Engineering Knowledge**
   - System design principles (ratios, flow rates)
   - Equipment specifications
   - Plumbing and mechanical

4. **Operational Knowledge**
   - Troubleshooting guides
   - Maintenance schedules
   - Harvest procedures

5. **Experiential Knowledge**
   - What worked/failed in your system
   - Community learnings
   - Optimization discoveries

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Set up project structure
- [ ] Install ChromaDB
- [ ] Build PDF extraction pipeline
- [ ] Create basic storage/retrieval functions
- [ ] Test with 2-3 source documents

### Phase 2: Core Functionality (Week 3-4)
- [ ] Implement chunking strategy
- [ ] Add metadata tracking
- [ ] Build query interface
- [ ] Create Python API for other projects
- [ ] Write tests

### Phase 3: Integration (Week 5-6)
- [ ] Connect to sensor system
- [ ] Expose REST API (optional)
- [ ] Add bulk document ingestion
- [ ] Create admin/management tools

### Phase 4: Enhancement (Ongoing)
- [ ] Add more documents
- [ ] Implement learning from system data
- [ ] Version control for knowledge
- [ ] Export/sharing capabilities

---

## Technical Stack

**Core:**
- Python 3.9+
- ChromaDB (vector database)
- sentence-transformers (embeddings)

**PDF Processing:**
- pymupdf / pdfplumber
- unstructured (optional, for complex layouts)

**API:**
- FastAPI (if REST needed)
- Direct Python imports (for local projects)

**Optional:**
- LangChain (for advanced RAG patterns)
- OpenAI/Anthropic API (for embedding generation)

---

## Success Criteria

This project is successful when:

1. ✅ Sensor system can query: "What does pH 6.2 mean for my lettuce?"
2. ✅ Teaching interface can retrieve: "Explain the nitrogen cycle"
3. ✅ New PDFs can be added in <5 minutes
4. ✅ Knowledge persists across system restarts
5. ✅ Retrieval returns relevant results in <1 second
6. ✅ Other developers can use the API without reading code

---

## Getting Started

```bash
# Clone and setup
git clone [your-repo]
cd aquaponics-knowledge-base
pip install -r requirements.txt

# Initialize database
python src/storage/db_manager.py init

# Ingest first document
python src/ingestion/process_pdf.py data/raw/aquaponics_textbook.pdf

# Test retrieval
python examples/example_queries.py
```

---

## Future Vision

This knowledge base becomes:
- **The librarian** for all aquaponics AI decisions
- **The teacher** for new users learning the system
- **The repository** for community-contributed knowledge
- **The foundation** for simulation accuracy
- **Portable** - share knowledge across systems/users

---

## Notes

- Start with 5-10 key documents you've already read
- Focus on retrieval quality over quantity initially
- Knowledge base should be READ ONLY for automated systems (humans curate additions)
- Consider privacy: some operational data may be personal/proprietary

---

**This is the brain. The sensors are the senses. Together, they think.**
