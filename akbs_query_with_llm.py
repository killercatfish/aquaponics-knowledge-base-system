#!/usr/bin/env python3
"""
AKBS Query with Ollama LLM
Retrieves context from knowledge base, then uses Ollama for generation
"""

import chromadb
from chromadb.config import Settings
import subprocess
from pathlib import Path

class AKBSWithLLM:
    def __init__(self, db_path="./data/knowledge_db", ollama_model="phi3:mini"):
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(name="aquaponics_knowledge")
        self.ollama_model = ollama_model
        
        # Get collection stats
        count = self.collection.count()
        print(f"✓ Connected to knowledge base")
        print(f"✓ {count} chunks available for queries\n")
        
    def query_with_llm(self, question, n_results=1):
        """Query knowledge base and generate answer with Ollama"""
        
        # Step 1: Retrieve relevant context from ChromaDB
        print(f"🔍 Searching knowledge base for: '{question}'")
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        
        # Step 2: Extract text chunks
        if not results['documents'][0]:
            print("❌ No relevant information found in knowledge base")
            return None
            
        contexts = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        # Show what was retrieved
        print(f"✓ Found {len(contexts)} relevant chunks\n")
        for i, (meta, dist) in enumerate(zip(metadatas, distances), 1):
            relevance = 1 - dist  # Convert distance to relevance
            source = meta.get('source', 'Unknown')
            print(f"  [{i}] {source} (relevance: {relevance:.2f})")
        
        # Step 3: Build prompt with context
        context_text = "\n\n---\n\n".join([
            f"[Source: {meta.get('source', 'Unknown')}]\n{doc}"
            for doc, meta in zip(contexts, metadatas)
        ])
        
        prompt = f"""You are an aquaponics and recirculating aquaculture systems (RAS) expert. Answer the question based ONLY on the context provided from the knowledge base. Be specific, cite sources when possible, and include any relevant numbers or specifications.

CONTEXT FROM KNOWLEDGE BASE:
{context_text}

QUESTION: {question}

ANSWER (cite the source files when referencing information):"""

        # Step 4: Send to Ollama
        print(f"\n🤖 Generating answer with {self.ollama_model}...\n")
        
        try:
            result = subprocess.run(
                ["ollama", "run", self.ollama_model, prompt],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"❌ Ollama error: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Query timed out (>120s)")
            return None
        except FileNotFoundError:
            print("❌ Ollama not found. Is it installed?")
            print("   Run: curl -fsSL https://ollama.com/install.sh | sh")
            return None
    
    def interactive(self):
        """Interactive query loop"""
        print("=" * 60)
        print("🧠 AKBS + Ollama - RAS Knowledge Assistant")
        print("=" * 60)
        print(f"Model: {self.ollama_model}")
        print("Commands: 'quit' or 'q' to exit\n")
        
        while True:
            try:
                question = input("❓ Ask a question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                    
                if not question:
                    continue
                
                print()  # Blank line
                answer = self.query_with_llm(question)
                
                if answer:
                    print("=" * 60)
                    print("📖 ANSWER:")
                    print("=" * 60)
                    print(answer)
                    print("=" * 60)
                print()  # Blank line
                    
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    kb = AKBSWithLLM()
    kb.interactive()
