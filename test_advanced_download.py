#!/usr/bin/env python3
"""
Test advanced download techniques to bypass Cloudflare
"""

import requests
import time
from bs4 import BeautifulSoup

def test_advanced_download():
    """Try different techniques to download"""
    
    # Test יומא page ב עמוד א 
    massechet_num = 306
    amud_num = 3
    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_num}&fs=0"
    
    print(f"Testing URL: {url}")
    
    # Method 1: Enhanced headers with session
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive'
    }
    
    try:
        print("Method 1: Enhanced headers with session...")
        
        # First visit main site
        main_response = session.get("https://daf-yomi.com", headers=headers, timeout=30)
        print(f"Main site status: {main_response.status_code}")
        
        if main_response.status_code == 200:
            # Wait a bit
            time.sleep(2)
            
            # Now try the specific page
            response = session.get(url, headers=headers, timeout=30)
            print(f"Page status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"SUCCESS! Downloaded {len(response.text)} characters")
                
                # Check if it contains actual content
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.find('h1')
                steinsaltz = soup.find('h2', string=lambda text: text and 'פירוש שטיינזלץ' in text)
                
                print(f"Title found: {'Yes' if title else 'No'}")
                print(f"Steinsaltz section found: {'Yes' if steinsaltz else 'No'}")
                
                if title:
                    print(f"Title text: {title.get_text().strip()}")
                
                # Save for inspection
                with open('test_advanced_download.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("Saved test_advanced_download.html")
                
                return True
            else:
                print(f"Failed with status {response.status_code}")
                if response.status_code == 403:
                    print("Still getting 403 - Cloudflare is blocking")
        else:
            print(f"Main site failed with status {main_response.status_code}")
            
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Try without session, simple approach
    try:
        print("\nMethod 2: Simple approach...")
        simple_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=simple_headers, timeout=30)
        print(f"Simple approach status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"SUCCESS with simple approach! {len(response.text)} characters")
            return True
            
    except Exception as e:
        print(f"Method 2 failed: {e}")
    
    return False

if __name__ == "__main__":
    success = test_advanced_download()
    if not success:
        print("\nAll methods failed - the site is likely blocking all automated requests")
        print("This would explain why both the web app and manual scripts fail")
        print("You may need to run the scripts from a different network or use a VPN")