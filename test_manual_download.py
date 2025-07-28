#!/usr/bin/env python3
"""
Test the manual download exactly like your original script
"""

import requests
import os
import re
from bs4 import BeautifulSoup

def hebrew_to_amud_number(daf_hebrew, amud):
    """Convert Hebrew daf notation to amud number used by the site"""
    hebrew_numbers = {
        'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
        'יא': 11, 'יב': 12, 'יג': 13, 'יד': 14, 'טו': 15, 'טז': 16, 'יז': 17, 'יח': 18, 'יט': 19, 'כ': 20,
        'כא': 21, 'כב': 22, 'כג': 23, 'כד': 24, 'כה': 25, 'כו': 26, 'כז': 27, 'כח': 28, 'כט': 29, 'ל': 30,
        'לא': 31, 'לב': 32, 'לג': 33, 'לד': 34, 'לה': 35, 'לו': 36, 'לז': 37, 'לח': 38, 'לט': 39, 'מ': 40,
        'מא': 41, 'מב': 42, 'מג': 43, 'מד': 44, 'מה': 45, 'מו': 46, 'מז': 47, 'מח': 48, 'מט': 49, 'נ': 50,
    }
    
    page_num = hebrew_numbers.get(daf_hebrew, 0)
    if amud == 'א':
        return (page_num - 1) * 2 + 1
    else:
        return (page_num - 1) * 2 + 2

def download_daf_page(massechet_num, amud_num):
    """Download a single daf page - EXACT copy from your original script"""
    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_num}&fs=0"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def extract_content_and_title(html_content):
    """Extract the Hebrew title and פירוש שטיינזלץ content - EXACT copy from original"""
    if not html_content:
        return None, None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract Hebrew title (like "שבועות מט ע\"א")
    title_element = soup.find('h1')
    if title_element:
        title = title_element.get_text().strip()
    else:
        title = "Unknown"
    
    # Find the פירוש שטיינזלץ section
    steinsaltz_section = None
    
    # Look for heading with "פירוש שטיינזלץ"
    steinsaltz_heading = soup.find('h2', string=lambda text: text and 'פירוש שטיינזלץ' in text)
    if steinsaltz_heading:
        # Get the parent container that contains the content
        steinsaltz_section = steinsaltz_heading.find_parent()
        if steinsaltz_section:
            # Find the content div that follows
            content_div = steinsaltz_section.find('div')
            if content_div:
                steinsaltz_section = content_div
    
    return title, steinsaltz_section

if __name__ == "__main__":
    print("Testing manual download with יומא (which we don't have locally)")
    
    # Test יומא page ב עמוד א - this should work like your original scripts
    massechet_num = 306  # יומא
    daf_hebrew = 'ב'
    amud = 'א'
    
    amud_num = hebrew_to_amud_number(daf_hebrew, amud)
    print(f"Trying to download יומא {daf_hebrew} {amud} (amud_num={amud_num})")
    
    html_content = download_daf_page(massechet_num, amud_num)
    
    if html_content:
        print(f"SUCCESS! Downloaded {len(html_content)} characters")
        
        title, content = extract_content_and_title(html_content)
        print(f"Title: {title}")
        print(f"Content found: {'Yes' if content else 'No'}")
        
        if title and content:
            print(f"SUCCESS! Both title and content extracted")
            # Save a sample
            with open('test_manual_yoma.html', 'w', encoding='utf-8') as f:
                f.write(f"<h1>{title}</h1>\n{str(content)}")
            print("Saved test_manual_yoma.html")
        else:
            print("FAILED to extract title or content")
    else:
        print("FAILED to download")