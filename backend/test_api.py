import requests
import os

def test_api():
    """Test the API with sample files"""
    
    # Test with CSV file
    csv_file = "sample_files/sample_invoices.csv"
    if os.path.exists(csv_file):
        print("Testing CSV file upload...")
        
        with open(csv_file, 'rb') as f:
            files = {'files': ('test.csv', f, 'text/csv')}
            
            try:
                response = requests.post('http://127.0.0.1:8000/upload', files=files)
                print(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"Response keys: {list(result.keys())}")
                    print(f"Data count: {len(result.get('data', []))}")
                    print(f"Stats: {result.get('stats', {})}")
                    
                    # Check each data item
                    for i, item in enumerate(result.get('data', [])):
                        print(f"Item {i+1}: {item}")
                        print(f"  Amount: '{item.get('amount')}' (type: {type(item.get('amount'))})")
                        print(f"  Amount empty?: {not item.get('amount')}")
                        print()
                else:
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"Request error: {e}")
    
    # Test with text file
    txt_file = "sample_files/sample_invoice_image.txt"
    if os.path.exists(txt_file):
        print("\nTesting text file upload...")
        
        with open(txt_file, 'rb') as f:
            files = {'files': ('test.txt', f, 'text/plain')}
            
            try:
                response = requests.post('http://127.0.0.1:8000/upload', files=files)
                print(f"Status code: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    data = result.get('data', [])
                    if data:
                        item = data[0] 
                        print(f"Text file result: {item}")
                        print(f"  Amount: '{item.get('amount')}' (type: {type(item.get('amount'))})")
                else:
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"Request error: {e}")

if __name__ == "__main__":
    test_api()