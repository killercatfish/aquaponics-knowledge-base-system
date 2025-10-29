#!/usr/bin/env python3
"""
AKBS Interactive Query Interface
Query your aquaponics knowledge base from the command line
"""

from akbs_ingest_markdown import AKBSIngester
import sys

def interactive_query_loop():
    """Run interactive query session"""
    
    # Initialize knowledge base
    print("\n" + "="*60)
    print("AQUAPONICS KNOWLEDGE BASE - Interactive Query")
    print("="*60)
    
    ingester = AKBSIngester(db_path="./data/knowledge_db")
    
    print(f"\nKnowledge Base loaded with {ingester.collection.count()} document chunks")
    print("\nType your questions below (or 'quit' to exit)")
    print("Examples:")
    print("  - What is the optimal pH for lettuce?")
    print("  - How do I manage dissolved oxygen?")
    print("  - What temperature do tilapia need?")
    print("="*60 + "\n")
    
    while True:
        try:
            # Get query from user
            query = input("\n🔍 Your question: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 🌱")
                break
            
            # Query the knowledge base
            results = ingester.query(query, n_results=3)
            
            # Display results
            ingester.pretty_print_results(results)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 🌱")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

def single_query(query_text: str):
    """Run a single query and exit"""
    ingester = AKBSIngester(db_path="./data/knowledge_db")
    results = ingester.query(query_text, n_results=3)
    ingester.pretty_print_results(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single query mode from command line
        query = " ".join(sys.argv[1:])
        single_query(query)
    else:
        # Interactive mode
        interactive_query_loop()
