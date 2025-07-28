#!/usr/bin/env python3
"""
Test the original download functionality directly
"""

import requests
from bs4 import BeautifulSoup

def hebrew_to_amud_number(daf_hebrew, amud):
    """Convert Hebrew daf notation to amud number used by the site"""
    hebrew_numbers = {
        'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    }
    
    page_num = hebrew_numbers.get(daf_hebrew, 0)
    if amud == 'א':
        return (page_num - 1) * 2 + 1
    else:  # ב
        return (page_num - 1) * 2 + 2

def download_daf_page(massechet_num, amud_num):
    """Download a single daf page"""
    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_num}&fs=0"
    print(f"Trying URL: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Response status: {response.status_code}")
        response.raise_for_status()
        print(f"Content length: {len(response.text)}")
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

if __name__ == "__main__":
    # Test עבודה זרה דף ב עמוד א (exactly like the original script)
    massechet_num = 309
    daf_hebrew = 'ב'
    amud = 'א'
    
    amud_num = hebrew_to_amud_number(daf_hebrew, amud)
    print(f"Converting {daf_hebrew} {amud} to amud number: {amud_num}")
    
    html_content = download_daf_page(massechet_num, amud_num)
    
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find('h1')
        if title:
            print(f"Success! Title: {title.get_text().strip()}")
        else:
            print("Success but no title found")
    else:
        print("Failed to download")