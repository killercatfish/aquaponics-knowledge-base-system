# AKBS Integration Roadmap
## Connecting Knowledge Base to Sensor System

**Last Updated:** 2025-11-06  
**Status:** ✅ AKBS Complete, Ready for Integration

---

## 🎯 IMMEDIATE NEXT STEPS

### Phase 1: Basic Integration (This Week) ⏳
- [ ] Create LLM interface in AquaponicAISystem
- [ ] Import AKBS query functions
- [ ] Test basic sensor → knowledge query
- [ ] Add "Get Info" links on dashboard

### Phase 2: Fast Retrieval (Next Week) 
- [ ] Integrate `akbs_query.py` into sensor system
- [ ] Add context-aware queries (include sensor values)
- [ ] Display relevant chunks on dashboard
- [ ] Add source citations with links

### Phase 3: "Ask AI" Button (Future - Optional)
- [ ] Add optional LLM generation button
- [ ] Use phi3:mini for faster responses (~30s)
- [ ] Show loading spinner during generation
- [ ] Cache common queries
- [ ] Consider running Ollama on Mac for faster responses

---

## 📋 INTEGRATION DETAILS

### Files to Create in AquaponicAISystem:

**1. `src/hydroponics/akbs/interface.py`**
```python
# Interface to AKBS knowledge base
# Import from ~/aquaponics-knowledge-base-system
```

**2. Update `src/hydroponics/core/main.py`**
```python
# Add AKBS query endpoints
# /api/knowledge/query
# /api/knowledge/ask-ai (optional, slow)
```

**3. Update `templates/dashboard.html`**
```javascript
// Add "More Info" buttons next to sensor readings
// Add "Ask AI" modal (optional)
```

---

## 🔗 INTEGRATION ARCHITECTURE
```
Sensor System (AquaponicAISystem)
    ↓
src/hydroponics/akbs/interface.py
    ↓
~/aquaponics-knowledge-base-system/akbs_query.py (FAST)
    ↓
ChromaDB → Returns relevant chunks (instant)

Optional slow path:
    ↓
~/aquaponics-knowledge-base-system/akbs_query_with_llm.py (SLOW)
    ↓
Ollama → Natural language response (30s)
```

---

## ✅ COMPLETED

- [x] AKBS code deployed to Pi
- [x] Dependencies installed
- [x] 79 RAS files ingested
- [x] 5,354 chunks in ChromaDB
- [x] Fast retrieval tested and working
- [x] LLM generation tested (slow but works)
- [x] phi3:mini pulled (29s response time)

---

## 🎯 SUCCESS CRITERIA

**Phase 1 Complete When:**
- Sensor dashboard has "Get Info" links
- Links show relevant knowledge base chunks
- Response time < 1 second
- Source citations included

**Phase 2 Complete When:**
- Queries include sensor context
- "pH is 6.2, what does this mean?" returns relevant info
- Multiple chunks displayed for context
- User can read full source documents

**Phase 3 Complete When:**
- Optional "Ask AI" button available
- Natural language explanations generated
- Loading indicator shows progress
- Reasonable response time achieved

---

## 📝 NOTES

**Why Retrieval-First:**
- Instant responses (<1s vs 30s)
- No hallucinations (exact textbook quotes)
- Source citations build trust
- Technical users prefer raw data
- LLM is polish, not core functionality

**When to Add LLM:**
- Educational interface needs explanations
- User testing shows demand
- Faster hardware available
- Grant demo requires "wow factor"

**Hardware Considerations:**
- Pi 5: phi3:mini ~30s per query
- Mac M-series: llama3.2 ~3s per query
- Could run Ollama on Mac, Pi queries via HTTP

---

## 🔗 RELATED DOCUMENTS

- **AKBS Setup:** `AKBS_SETUP_GUIDE.md`
- **Query Examples:** `test_akbs.py`
- **Sensor System:** `~/AquaponicAISystem/`
- **Project Vision:** `/mnt/project/Master_System_Overview_v2.md`
- **Grant Strategy:** `/mnt/project/GRANT_STRATEGY_TABLE_OF_CONTENTS.md`

---

**Remember:** The knowledge base itself is the achievement. The LLM is optional polish.
