#!/bin/bash
# AKBS Setup Script
# Demonstrates code/data separation

echo "=================================="
echo "AKBS Setup - Code vs Data"
echo "=================================="

# Create directory structure
echo ""
echo "Creating directory structure..."
mkdir -p data/knowledge_db
mkdir -p processed-chapters
mkdir -p raw-pdfs

echo "✓ Created: data/knowledge_db (gitignored)"
echo "✓ Created: processed-chapters (gitignored)"  
echo "✓ Created: raw-pdfs (gitignored)"

# Show what's tracked by git
echo ""
echo "=================================="
echo "What Git Tracks (Public Code):"
echo "=================================="
ls -lh *.py *.md requirements.txt .gitignore 2>/dev/null | grep -v total

echo ""
echo "=================================="
echo "What Git Ignores (Private Data):"
echo "=================================="
echo "  - data/ directory (your knowledge base)"
echo "  - processed-chapters/ (your markdown files)"
echo "  - raw-pdfs/ (your source documents)"

# Verify gitignore
echo ""
echo "=================================="
echo "Verifying .gitignore protection:"
echo "=================================="

if [ -f .gitignore ]; then
    if git check-ignore data/ > /dev/null 2>&1; then
        echo "✓ data/ is protected by .gitignore"
    else
        echo "⚠ Warning: data/ might not be ignored"
    fi
    
    if git check-ignore processed-chapters/ > /dev/null 2>&1; then
        echo "✓ processed-chapters/ is protected by .gitignore"
    else
        echo "⚠ Warning: processed-chapters/ might not be ignored"
    fi
else
    echo "⚠ .gitignore not found - create it first!"
fi

echo ""
echo "=================================="
echo "Next Steps:"
echo "=================================="
echo "1. Put your markdown files in: processed-chapters/"
echo "2. Run: python akbs_ingest_markdown.py"
echo "3. Your data stays local, code can be shared!"
echo ""
echo "Git commands:"
echo "  git add *.py *.md requirements.txt .gitignore"
echo "  git commit -m 'Initial AKBS setup'"
echo ""
echo "Your data will NOT be committed (protected by .gitignore)"
echo "=================================="
