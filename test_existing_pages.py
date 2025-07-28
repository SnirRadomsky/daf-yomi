#!/usr/bin/env python3
"""
Test the web app with pages that actually exist in the pages/ directory
"""

import requests
import json

def test_existing_pages():
    """Test with pages that exist: עבודה זרה סב-סג"""
    print("Testing with existing pages: עבודה זרה סב-סג")
    
    url = "http://localhost:5001/api/download"
    data = {
        "tractate": "עבודה זרה",
        "start_daf": "סב",
        "start_amud": "א",
        "end_daf": "סג", 
        "end_amud": "ב"
    }
    
    try:
        response = requests.post(url, json=data, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Found existing pages!")
            print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Save the downloaded file for verification
            with open('test_existing_pages.html', 'wb') as f:
                f.write(response.content)
            print("📄 Downloaded file saved as 'test_existing_pages.html'")
            
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_existing_pages()