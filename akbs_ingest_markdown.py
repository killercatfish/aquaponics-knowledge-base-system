#!/usr/bin/env python3
"""
AKBS Markdown Ingestion Pipeline
Ingests Claude-processed textbook markdown files into ChromaDB
"""

import chromadb
from chromadb.config import Settings
from pathlib import Path
import re
from typing import List, Dict, Optional
from datetime import datetime
import hashlib

class AKBSIngester:
    """Ingest processed markdown files into persistent knowledge base"""
    
    def __init__(self, db_path: str = "./data/knowledge_db"):
        """
        Initialize the ingester with persistent ChromaDB
        
        Args:
            db_path: Path to store the ChromaDB database
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="aquaponics_knowledge",
            metadata={"description": "Aquaponics domain knowledge from textbooks and papers"}
        )
        
        print(f"✓ Initialized AKBS with database at: {self.db_path}")
        print(f"✓ Current documents in collection: {self.collection.count()}")
    
    def extract_metadata_from_filename(self, filepath: Path) -> Dict[str, str]:
        """
        Extract metadata from filename
        Expected format: Chapter-##-Title-Type.md
        """
        filename = filepath.stem
        metadata = {
            'filename': filepath.name,
            'filepath': str(filepath),
            'ingested_at': datetime.now().isoformat()
        }
        
        # Try to extract chapter number
        chapter_match = re.search(r'Chapter-(\d+)', filename)
        if chapter_match:
            metadata['chapter'] = chapter_match.group(1)
        
        # Detect document type
        if 'Readable' in filename:
            metadata['type'] = 'readable'
        elif 'AI-Tagged' in filename:
            metadata['type'] = 'ai_tagged'
        elif 'Quick-Reference' in filename:
            metadata['type'] = 'quick_reference'
        else:
            metadata['type'] = 'general'
        
        return metadata
    
    def extract_xml_tags(self, text: str) -> Dict[str, List[str]]:
        """
        Extract content from XML tags in AI-tagged files
        Returns dict of tag_name: [contents]
        """
        tags = {}
        
        # Common tags from the workflow
        tag_patterns = [
            'parameter', 'value', 'range', 'optimal',
            'diagram', 'table', 'formula', 'critical',
            'takeaway', 'cross_reference'
        ]
        
        for tag in tag_patterns:
            pattern = f'<{tag}>(.*?)</{tag}>'
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                tags[tag] = matches
        
        return tags
    
    def chunk_markdown(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Split markdown into semantic chunks based on headers and content
        
        Args:
            text: Markdown text to chunk
            max_chunk_size: Approximate maximum characters per chunk
        """
        chunks = []
        
        # Split by headers (##, ###, etc)
        sections = re.split(r'\n(?=#{1,6}\s)', text)
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # If section is small enough, keep as is
            if len(section) <= max_chunk_size:
                chunks.append(section)
            else:
                # Split long sections by paragraphs
                paragraphs = section.split('\n\n')
                current_chunk = ""
                
                for para in paragraphs:
                    if len(current_chunk) + len(para) <= max_chunk_size:
                        current_chunk += para + "\n\n"
                    else:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = para + "\n\n"
                
                if current_chunk:
                    chunks.append(current_chunk.strip())
        
        return chunks
    
    def generate_chunk_id(self, chunk: str, metadata: Dict) -> str:
        """Generate unique ID for chunk based on content and metadata"""
        content = f"{metadata.get('filename', '')}_{chunk[:100]}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def ingest_file(self, filepath: Path, source_name: Optional[str] = None):
        """
        Ingest a single markdown file into the knowledge base
        
        Args:
            filepath: Path to markdown file
            source_name: Optional name of source (e.g., "RAS Textbook")
        """
        print(f"\nProcessing: {filepath.name}")
        
        # Read file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract metadata
        metadata = self.extract_metadata_from_filename(filepath)
        if source_name:
            metadata['source'] = source_name
        
        # Extract XML tags if present
        xml_tags = self.extract_xml_tags(content)
        if xml_tags:
            metadata['has_tags'] = ','.join(xml_tags.keys())
        
        # Chunk the content
        chunks = self.chunk_markdown(content)
        print(f"  → Split into {len(chunks)} chunks")
        
        # Prepare for ChromaDB
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = self.generate_chunk_id(chunk, metadata)
            ids.append(chunk_id)
            documents.append(chunk)
            
            # Add chunk-specific metadata
            chunk_metadata = metadata.copy()
            chunk_metadata['chunk_index'] = str(i)
            chunk_metadata['total_chunks'] = str(len(chunks))
            metadatas.append(chunk_metadata)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"  ✓ Added {len(chunks)} chunks to knowledge base")
    
    def ingest_directory(self, directory: Path, source_name: Optional[str] = None, pattern: str = "*.md"):
        """
        Ingest all markdown files from a directory
        
        Args:
            directory: Path to directory containing markdown files
            source_name: Optional name of source
            pattern: File pattern to match (default: *.md)
        """
        directory = Path(directory)
        files = list(directory.glob(pattern))
        
        print(f"\n{'='*60}")
        print(f"Ingesting files from: {directory}")
        print(f"Found {len(files)} matching files")
        print(f"{'='*60}")
        
        for filepath in files:
            try:
                self.ingest_file(filepath, source_name)
            except Exception as e:
                print(f"  ✗ Error processing {filepath.name}: {e}")
        
        print(f"\n{'='*60}")
        print(f"Ingestion complete!")
        print(f"Total documents in collection: {self.collection.count()}")
        print(f"{'='*60}\n")
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """
        Query the knowledge base
        
        Args:
            query_text: Natural language query
            n_results: Number of results to return
        
        Returns:
            Dictionary with documents, metadatas, and distances
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        return {
            'documents': results['documents'][0],
            'metadatas': results['metadatas'][0],
            'distances': results['distances'][0]
        }
    
    def pretty_print_results(self, results: Dict):
        """Print query results in a readable format"""
        print(f"\n{'='*60}")
        print(f"Found {len(results['documents'])} relevant chunks:")
        print(f"{'='*60}\n")
        
        for i, (doc, meta, dist) in enumerate(zip(
            results['documents'], 
            results['metadatas'], 
            results['distances']
        ), 1):
            print(f"Result {i} (relevance: {1-dist:.2f})")
            print(f"Source: {meta.get('filename', 'Unknown')}")
            if 'chapter' in meta:
                print(f"Chapter: {meta['chapter']}")
            print(f"Type: {meta.get('type', 'Unknown')}")
            print(f"\nContent preview:")
            print("-" * 60)
            # Show first 300 chars
            preview = doc[:300] + "..." if len(doc) > 300 else doc
            print(preview)
            print("=" * 60 + "\n")


def main():
    """Ingest all RAS knowledge base markdown files"""
    ingester = AKBSIngester(db_path="./data/knowledge_db")
    
    print("\n" + "=" * 60)
    print("INGESTING RAS EXPERT KNOWLEDGE BASE")
    print("=" * 60 + "\n")
    
    base_path = Path("./processed-chapters")
    
    # Define subdirectories to process
    directories = [
        "0-Master-Files",
        "2-Processed-Chapters", 
        "3-Topic-Guides",
        "4-Quick-References",
        "5-Diagrams",
        "6-AI-Tools"
    ]
    
    total_files = 0
    
    for subdir in directories:
        full_path = base_path / subdir
        if full_path.exists():
            print(f"\n{'='*60}")
            print(f"Processing: {subdir}")
            print('='*60)
            
            # Count files first
            md_files = list(full_path.glob("*.md"))
            print(f"Found {len(md_files)} markdown files\n")
            
            ingester.ingest_directory(
                full_path, 
                source_name=f"RAS-{subdir}"
            )
            total_files += len(md_files)
    
    # Also ingest root-level files (README, etc)
    print(f"\n{'='*60}")
    print("Processing: Root-level documentation")
    print('='*60)
    root_files = [f for f in base_path.glob("*.md") if f.is_file()]
    if root_files:
        for file in root_files:
            print(f"Processing: {file.name}")
            ingester.ingest_file(file, source_name="RAS-Root-Docs")
        total_files += len(root_files)
    
    print("\n" + "=" * 60)
    print("✓ INGESTION COMPLETE!")
    print("=" * 60)
    print(f"Total files processed: {total_files}")
    print(f"Database location: ./data/knowledge_db")
    print("\nYou can now query the knowledge base with:")
    print("  python akbs_query.py")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()