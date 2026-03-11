#!/usr/bin/env python3
"""
Debug script to test invoice extraction
"""
import asyncio
import sys
import os
import traceback

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from extractor import extract_invoice, extractor
    from config import config
    print("✅ Modules imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    traceback.print_exc()
    sys.exit(1)

async def test_extraction():
    """Test the extraction with sample files"""
    
    print("=== Invoice Extraction Debug ===")
    print(f"Gemini API available: {config.is_available()}")
    print(f"API Key configured: {bool(config.api_key and config.api_key != 'your_gemini_api_key_here')}")
    print(f"Model: {config.model_name}")
    print(f"Fallback enabled: {config.fallback_to_traditional}")
    print()
    
    # Test with sample text file (simulating image content)
    sample_file = "../sample_files/sample_invoice_image.txt"
    if os.path.exists(sample_file):
        print(f"Testing with: {sample_file}")
        
        # Read the content as text and test Gemini directly
        with open(sample_file, 'r') as f:
            content = f.read()
            print(f"File content length: {len(content)} characters")
            print("Content preview:", content[:200] + "..." if len(content) > 200 else content)
            print()
            
        # Test Gemini extraction directly
        if config.is_available():
            print("Testing Gemini extraction...")
            try:
                result = await extractor.extract_with_gemini(content)
                print(f"Gemini result: {result}")
            except Exception as e:
                print(f"Gemini error: {e}")
            print()
        
        # Test traditional parsing
        print("Testing traditional parsing...")
        traditional_result = extractor.parse_text_traditional(content)
        print(f"Traditional result: {traditional_result}")
        print()
    
    # Test with CSV file
    csv_file = "../sample_files/sample_invoices.csv"
    if os.path.exists(csv_file):
        print(f"Testing with: {csv_file}")
        result = await extract_invoice(csv_file)
        print(f"CSV extraction result: {result}")
        print()

if __name__ == "__main__":
    try:
        asyncio.run(test_extraction())
    except Exception as e:
        print(f"❌ Error running test: {e}")
        traceback.print_exc()