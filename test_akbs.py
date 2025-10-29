#!/usr/bin/env python3
"""
AKBS Test Script
Verify that your installation is working correctly
"""

import sys
from pathlib import Path

def test_imports():
    """Test that required packages are installed"""
    print("Testing imports...")
    try:
        import chromadb
        print("  ✓ chromadb installed")
    except ImportError:
        print("  ✗ chromadb not found - run: pip install chromadb")
        return False
    
    try:
        import sentence_transformers
        print("  ✓ sentence-transformers installed")
    except ImportError:
        print("  ✗ sentence-transformers not found - run: pip install sentence-transformers")
        return False
    
    return True

def test_akbs_module():
    """Test that AKBS module can be imported"""
    print("\nTesting AKBS module...")
    try:
        from akbs_ingest_markdown import AKBSIngester
        print("  ✓ akbs_ingest_markdown module loaded")
        return True
    except ImportError as e:
        print(f"  ✗ Cannot import AKBS module: {e}")
        return False

def test_database_creation():
    """Test that database can be created"""
    print("\nTesting database creation...")
    try:
        from akbs_ingest_markdown import AKBSIngester
        ingester = AKBSIngester(db_path="./test_db")
        print(f"  ✓ Database created successfully")
        print(f"  ✓ Documents in database: {ingester.collection.count()}")
        return True
    except Exception as e:
        print(f"  ✗ Database creation failed: {e}")
        return False

def test_sample_ingestion():
    """Test ingestion with sample markdown"""
    print("\nTesting sample ingestion...")
    try:
        from akbs_ingest_markdown import AKBSIngester
        
        # Create sample markdown
        sample_md = Path("./test_sample.md")
        sample_content = """# Sample Chapter: pH Management

## Optimal pH Ranges

For leafy greens like lettuce, the optimal pH range is 5.5 to 6.5.

<parameter>pH</parameter>
<optimal>5.5-6.5</optimal>
<crop>lettuce</crop>

## Adjusting pH

If pH is too high, add acid. If pH is too low, add base.
"""
        sample_md.write_text(sample_content)
        
        # Ingest it
        ingester = AKBSIngester(db_path="./test_db")
        ingester.ingest_file(sample_md, source_name="Test")
        
        print(f"  ✓ Sample file ingested successfully")
        print(f"  ✓ Documents in database: {ingester.collection.count()}")
        
        # Clean up
        sample_md.unlink()
        
        return True
    except Exception as e:
        print(f"  ✗ Ingestion test failed: {e}")
        return False

def test_query():
    """Test querying the database"""
    print("\nTesting query functionality...")
    try:
        from akbs_ingest_markdown import AKBSIngester
        
        ingester = AKBSIngester(db_path="./test_db")
        
        if ingester.collection.count() == 0:
            print("  ⚠ No documents in database to query")
            return True
        
        results = ingester.query("optimal pH for lettuce", n_results=1)
        
        if results['documents']:
            print(f"  ✓ Query successful!")
            print(f"  ✓ Found {len(results['documents'])} result(s)")
            print(f"\n  Sample result:")
            print(f"  {results['documents'][0][:100]}...")
            return True
        else:
            print("  ⚠ Query returned no results (but query worked)")
            return True
            
    except Exception as e:
        print(f"  ✗ Query test failed: {e}")
        return False

def cleanup():
    """Clean up test files"""
    print("\nCleaning up test files...")
    try:
        import shutil
        test_db = Path("./test_db")
        if test_db.exists():
            shutil.rmtree(test_db)
        print("  ✓ Test database removed")
    except Exception as e:
        print(f"  ⚠ Cleanup warning: {e}")

def main():
    print("="*60)
    print("AKBS INSTALLATION TEST")
    print("="*60)
    
    tests = [
        ("Package Installation", test_imports),
        ("AKBS Module", test_akbs_module),
        ("Database Creation", test_database_creation),
        ("Sample Ingestion", test_sample_ingestion),
        ("Query Functionality", test_query),
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    cleanup()
    
    all_passed = all(r for _, r in results)
    
    print("="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou're ready to use AKBS!")
        print("\nNext steps:")
        print("  1. Put your markdown files in a directory")
        print("  2. Edit akbs_ingest_markdown.py with your paths")
        print("  3. Run: python akbs_ingest_markdown.py")
        print("  4. Query: python akbs_query.py")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above and run again.")
        print("\nCommon fixes:")
        print("  - Install dependencies: pip install -r requirements.txt")
        print("  - Check file permissions")
        print("  - Make sure you're in the right directory")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
