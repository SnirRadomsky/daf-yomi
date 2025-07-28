#!/usr/bin/env python3
"""
Test just the download function from web app
"""

import requests
import os

def download_daf_page(massechet_num, amud_num):
    """Download a single daf page - EXACTLY like web app"""
    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_num}&fs=0"
    
    # Use EXACT same headers as web app
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Attempting real download: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print(f"SUCCESS: Downloaded {len(response.text)} characters from real site")
        return response.text
    except requests.RequestException as e:
        print(f"Real download failed: {e}")
        return None

if __name__ == "__main__":
    print("Testing web app download function directly...")
    
    # Test יומא page ב עמוד א 
    massechet_num = 306  # יומא
    amud_num = 3  # ב א
    
    result = download_daf_page(massechet_num, amud_num)
    
    if result:
        print(f"SUCCESS! Web app function downloaded {len(result)} characters")
        # Save for comparison
        with open('test_webapp_function.html', 'w', encoding='utf-8') as f:
            f.write(result)
        print("Saved test_webapp_function.html")
    else:
        print("FAILED: Web app function failed")