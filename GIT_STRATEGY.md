# Git Strategy for AKBS

## TL;DR

✅ **Code goes in git** (share this!)
❌ **Data stays local** (private to you)

The `.gitignore` file keeps your textbook content and knowledge base private automatically.

---

## What Gets Committed to Git

```
aquaponics-knowledge-base/
├── .gitignore                    ✅ COMMIT (protects your data)
├── README.md                     ✅ COMMIT (documentation)
├── requirements.txt              ✅ COMMIT (dependencies)
├── akbs_ingest_markdown.py      ✅ COMMIT (code)
├── akbs_query.py                 ✅ COMMIT (code)
├── test_akbs.py                  ✅ COMMIT (code)
├── AKBS_SETUP_GUIDE.md          ✅ COMMIT (documentation)
├── AKBS_Project_Spec.md         ✅ COMMIT (documentation)
├── QUICK_REFERENCE.md           ✅ COMMIT (documentation)
└── FILE_INDEX.md                 ✅ COMMIT (documentation)
```

---

## What Stays LOCAL (Never Committed)

```
aquaponics-knowledge-base/
├── data/                         ❌ LOCAL (your knowledge base)
│   └── knowledge_db/            ❌ LOCAL (ChromaDB files)
├── processed-chapters/           ❌ LOCAL (your markdown files)
├── textbooks/                    ❌ LOCAL (your PDFs)
└── any-directory-with-content/  ❌ LOCAL (your actual data)
```

**Why?**
- Your textbook content is copyrighted
- Your processed data is your work
- Knowledge base can be regenerated from source files
- Keeps repo size small
- Others can use the code with their own data

---

## Setup Git Repository

### Option 1: New Repository

```bash
# Initialize git
cd aquaponics-knowledge-base
git init

# Add all code files
git add .gitignore
git add *.py
git add *.md
git add requirements.txt

# First commit
git commit -m "Initial AKBS setup - code only, no data"

# Create GitHub repo (optional)
# Then push:
git remote add origin https://github.com/yourusername/aquaponics-knowledge-base.git
git push -u origin main
```

### Option 2: Add to Existing Repository

```bash
# If you already have a git repo
cd your-existing-repo

# Create akbs subdirectory
mkdir akbs
cd akbs

# Copy AKBS files here
cp /path/to/downloads/* .

# Add to git (data directories automatically ignored)
git add .
git commit -m "Add AKBS knowledge base system"
```

---

## Directory Structure (Git + Local)

### What Your Repo Looks Like

```
aquaponics-knowledge-base/     ← Git tracks this
├── .gitignore                 ← In git
├── README.md                  ← In git
├── *.py                       ← In git
├── *.md                       ← In git
└── requirements.txt           ← In git
```

### What Your Local Machine Has

```
aquaponics-knowledge-base/     
├── .gitignore                 ← In git
├── README.md                  ← In git
├── *.py                       ← In git
├── data/                      ← NOT in git (ignored)
│   └── knowledge_db/         ← NOT in git (ignored)
├── processed-chapters/        ← NOT in git (ignored)
│   ├── Chapter-01-*.md       ← NOT in git (ignored)
│   └── ...                    ← NOT in git (ignored)
└── textbooks/                 ← NOT in git (ignored)
    └── *.pdf                  ← NOT in git (ignored)
```

---

## Data Independence

### Each User Has Their Own Data

**Your Setup:**
```
you/aquaponics-knowledge-base/
├── code/ (from git)
└── data/ (your local textbooks)
```

**Someone Else's Setup:**
```
them/aquaponics-knowledge-base/
├── code/ (same code from git)
└── data/ (their different textbooks)
```

### Benefits

✅ **Share code openly** - Others can use your pipeline
✅ **Keep data private** - Your textbooks stay local
✅ **Portable** - Works anywhere with any data
✅ **Collaborative** - Others can improve the code
✅ **Legal** - No copyright issues pushing to GitHub

---

## Example Workflow

### Day 1: Setup
```bash
# Clone/download the code
git clone https://github.com/yourusername/akbs.git
cd akbs

# Your data directories don't exist yet (normal!)
# Create them:
mkdir -p data/knowledge_db
mkdir -p processed-chapters

# Put your markdown files in processed-chapters/
cp ~/textbooks/processed/*.md processed-chapters/
```

### Day 2: Use
```bash
# Install
pip install -r requirements.txt

# Ingest YOUR data (not in git)
python akbs_ingest_markdown.py

# Now data/ directory has your knowledge base
# But git ignores it!
git status  # Shows no data/ directory
```

### Day 3: Update Code
```bash
# Make improvements to code
vim akbs_ingest_markdown.py

# Commit code changes
git add akbs_ingest_markdown.py
git commit -m "Improved chunking algorithm"
git push

# Your data/ directory is untouched and still ignored
```

---

## Verifying Data Is Ignored

```bash
# Check what git sees
git status

# Should show:
#   ✅ Modified: akbs_ingest_markdown.py (if you changed code)
#   ❌ NOT showing: data/, processed-chapters/, *.pdf

# Check .gitignore is working
git check-ignore data/knowledge_db
# Output: data/knowledge_db (means it's ignored ✓)
```

---

## Sharing Your Knowledge Base (Optional)

If you WANT to share your processed knowledge with someone specific:

### Option 1: Zip the Data Directory
```bash
# Create archive of just the database
tar -czf my-aquaponics-kb.tar.gz data/knowledge_db/

# Send via email, Dropbox, etc. (NOT git)
```

### Option 2: Export/Import Feature (Future)
```python
# Future feature you could add:
kb.export("my-knowledge.zip")
# Send zip file separately
kb.import_from("received-knowledge.zip")
```

### Option 3: Regenerate from Source
```bash
# Share your processed markdown files separately
# They can ingest them to recreate the database
```

---

## Multi-Machine Workflow

### Computer 1 (Processing)
```bash
# Use Claude to process textbooks
# Creates: processed-chapters/*.md

# Commit code improvements
git add akbs_ingest_markdown.py
git commit -m "Added better metadata extraction"
git push
```

### Computer 2 (Raspberry Pi)
```bash
# Pull latest code
git pull

# Copy your data separately (rsync, scp, etc.)
rsync -av computer1:~/akbs/data/ ./data/
rsync -av computer1:~/akbs/processed-chapters/ ./processed-chapters/

# Use on Pi
python akbs_query.py
```

---

## Best Practices

### ✅ DO:
- Commit all `.py` files
- Commit all `.md` documentation
- Commit `requirements.txt`
- Commit `.gitignore`
- Keep data directories outside git

### ❌ DON'T:
- Commit `data/` directory
- Commit PDFs or markdown files
- Commit knowledge base files
- Remove `.gitignore`

### 💡 CONSIDER:
- Adding example data (tiny sample)
- Documenting your data sources (without sharing them)
- Creating setup instructions for others

---

## Example .git/config

```ini
[core]
    repositoryformatversion = 0
    filemode = true
    bare = false
    logallrefupdates = true
[remote "origin"]
    url = https://github.com/yourusername/aquaponics-knowledge-base.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
    remote = origin
    merge = refs/heads/main
```

---

## Troubleshooting

### "I accidentally committed data/"

```bash
# Remove from git but keep locally
git rm -r --cached data/
git commit -m "Remove data directory from git"
git push

# Verify .gitignore has data/ listed
cat .gitignore | grep data
```

### "Someone cloned my repo, can they see my data?"

No! If `.gitignore` was in place before you committed, your data never went to git.

### "I want to move my data to a different computer"

```bash
# Use rsync, scp, or manual copy
# NOT git
scp -r data/ othercomputer:~/akbs/data/
```

---

## Example GitHub README

If you push to GitHub, your README could say:

```markdown
# Aquaponics Knowledge Base System

Code for ingesting textbook content into a queryable knowledge base.

## Setup
1. Clone this repo
2. Add your own data to `data/` and `processed-chapters/`
3. Run `python akbs_ingest_markdown.py`

Note: This repo contains only code. Data directories are gitignored.
Users provide their own textbook content.
```

---

## Summary

| Item | In Git? | Private? | Portable? |
|------|---------|----------|-----------|
| Code (*.py) | ✅ Yes | ❌ Public | ✅ Yes |
| Docs (*.md) | ✅ Yes | ❌ Public | ✅ Yes |
| .gitignore | ✅ Yes | ❌ Public | ✅ Yes |
| data/ | ❌ No | ✅ Private | ⚠️  Manual |
| processed-chapters/ | ❌ No | ✅ Private | ⚠️  Manual |
| Knowledge base | ❌ No | ✅ Private | ⚠️  Manual |

---

**Your code is shareable. Your data is yours. Perfect separation.** ✨
