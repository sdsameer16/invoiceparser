#!/usr/bin/env python3
"""
Direct test of extraction functions
"""
import asyncio
import sys
import os

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

from extractor import extract_invoice

async def test_direct_extraction():
    """Test extraction functions directly"""
    
    print("=== Direct Extraction Test ===")
    
    # Test CSV file
    csv_file = "sample_files/sample_invoices.csv"
    print(f"Testing {csv_file}...")
    
    result1 = await extract_invoice(csv_file)
    print(f"CSV Result: {result1}")
    print(f"CSV Result type: {type(result1)}")
    
    if isinstance(result1, list):
        for i, item in enumerate(result1):
            print(f"Item {i+1}: {item}")
            amount = item.get('amount')
            print(f"  Amount value: '{amount}' (type: {type(amount)}, bool: {bool(amount)})")
    
    print("\n" + "="*50)
    
    # Test text file  
    txt_file = "sample_files/sample_invoice_image.txt"
    print(f"Testing {txt_file}...")
    
    result2 = await extract_invoice(txt_file)
    print(f"Text Result: {result2}")
    print(f"Text Result type: {type(result2)}")
    
    if isinstance(result2, dict):
        amount = result2.get('amount')
        print(f"  Amount value: '{amount}' (type: {type(amount)}, bool: {bool(amount)})")

if __name__ == "__main__":
    try:
        asyncio.run(test_direct_extraction())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()