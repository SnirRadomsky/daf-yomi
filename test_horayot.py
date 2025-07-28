#!/usr/bin/env python3
"""
Test with הוריות which definitely has files
"""

import requests
import json

def test_horayot():
    """Test with הוריות ה-ו"""
    print("Testing with הוריות ה-ו")
    
    url = "http://localhost:5001/api/download"
    data = {
        "tractate": "הוריות",
        "start_daf": "ה",
        "start_amud": "א",
        "end_daf": "ו", 
        "end_amud": "ב"
    }
    
    try:
        response = requests.post(url, json=data, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Found הוריות pages!")
            print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Save the downloaded file for verification
            with open('test_horayot.html', 'wb') as f:
                f.write(response.content)
            print("📄 Downloaded file saved as 'test_horayot.html'")
            
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_horayot()