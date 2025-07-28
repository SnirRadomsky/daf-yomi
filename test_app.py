#!/usr/bin/env python3
"""
Test script for the Daf Yomi web application
Tests both valid and invalid מסכת requests
"""

import requests
import json

def test_valid_tractate():
    """Test with a valid tractate - עבודה זרה"""
    print("Testing valid מסכת: עבודה זרה")
    
    url = "http://localhost:5001/api/download"
    data = {
        "tractate": "עבודה זרה",
        "start_daf": "ב",
        "start_amud": "א", 
        "end_daf": "ג",
        "end_amud": "ב"
    }
    
    try:
        response = requests.post(url, json=data, timeout=60)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Valid tractate request worked!")
            print(f"Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Save the downloaded file for verification
            with open('test_download_valid.html', 'wb') as f:
                f.write(response.content)
            print("📄 Downloaded file saved as 'test_download_valid.html'")
            
        else:
            print(f"❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

def test_invalid_tractate():
    """Test with an invalid tractate name"""
    print("\nTesting invalid מסכת: בלה בלה")
    
    url = "http://localhost:5001/api/download"
    data = {
        "tractate": "בלה בלה",  # Invalid tractate name
        "start_daf": "ב",
        "start_amud": "א",
        "end_daf": "ג", 
        "end_amud": "ב"
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            error_data = response.json()
            print("✅ SUCCESS: Invalid tractate properly rejected!")
            print(f"Error message: {error_data.get('error', 'No error message')}")
        else:
            print(f"❌ UNEXPECTED: Expected 400, got {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

def test_missing_parameters():
    """Test with missing parameters"""
    print("\nTesting missing parameters:")
    
    url = "http://localhost:5001/api/download"
    data = {
        "tractate": "עבודה זרה",
        # Missing start_daf, start_amud, end_daf, end_amud
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            error_data = response.json()
            print("✅ SUCCESS: Missing parameters properly rejected!")
            print(f"Error message: {error_data.get('error', 'No error message')}")
        else:
            print(f"❌ UNEXPECTED: Expected 400, got {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("🧪 Testing Daf Yomi Web Application")
    print("=" * 50)
    
    # Test 1: Valid tractate
    test_valid_tractate()
    
    # Test 2: Invalid tractate  
    test_invalid_tractate()
    
    # Test 3: Missing parameters
    test_missing_parameters()
    
    print("\n" + "=" * 50)
    print("🏁 Testing completed!")