#!/usr/bin/env python3
"""
Debug script to test the download URL structure
"""

import requests
from bs4 import BeautifulSoup

def test_url():
    """Test the actual URL structure"""
    # Let's try to use the existing download script's approach
    print("Testing with existing approach from download_daf_simple.py")
    
    # Test with עבודה זרה, page ב, amud א
    daf_hebrew = 'ב'
    amud = 'א'
    
    # Convert to amud number using the same logic
    page_num = 2  # ב = 2
    amud_number = (page_num - 1) * 2 + 1  # א = (2-1)*2 + 1 = 3
    
    # The original download script used massechet 309 for עבודה זרה
    # Let's try that
    massechet_num = 309
    
    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_number}&fs=0"
    print(f"Testing URL: {url}")
    
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        # First, visit the main page to establish session
        main_page = session.get("https://daf-yomi.com", headers=headers, timeout=30)
        print(f"Main page status: {main_page.status_code}")
        
        # Now try the specific page
        response = session.get(url, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1')
            if title:
                print(f"Title found: {title.get_text().strip()}")
            else:
                print("No h1 title found")
                
            # Look for פירוש שטיינזלץ
            steinsaltz = soup.find('h2', string=lambda text: text and 'פירוש שטיינזלץ' in text)
            if steinsaltz:
                print("✅ Found פירוש שטיינזלץ section")
            else:
                print("❌ No פירוש שטיינזלץ section found")
                # Let's see what h2 elements exist
                h2_elements = soup.find_all('h2')
                print(f"Found {len(h2_elements)} h2 elements:")
                for h2 in h2_elements[:5]:  # Show first 5
                    print(f"  - {h2.get_text().strip()[:50]}...")
        else:
            print(f"HTTP Error: {response.status_code}")
            print(response.text[:500])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_url()