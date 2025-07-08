#!/usr/bin/env python3
"""
Simple Daf Yomi content downloader
Downloads content directly from daf-yomi.com using HTTP requests
"""

import requests
import os
import re
from bs4 import BeautifulSoup

def hebrew_to_amud_number(daf_hebrew, amud):
    """Convert Hebrew daf notation to amud number used by the site"""
    # Mapping Hebrew letters to numbers
    hebrew_numbers = {
        'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
        'יא': 11, 'יב': 12, 'יג': 13, 'יד': 14, 'טו': 15, 'טז': 16, 'יז': 17, 'יח': 18, 'יט': 19, 'כ': 20,
        'כא': 21, 'כב': 22, 'כג': 23, 'כד': 24, 'כה': 25, 'כו': 26, 'כז': 27, 'כח': 28, 'כט': 29, 'ל': 30,
        'לא': 31, 'לב': 32, 'לג': 33, 'לד': 34, 'לה': 35, 'לו': 36, 'לז': 37, 'לח': 38, 'לט': 39, 'מ': 40,
        'מא': 41, 'מב': 42, 'מג': 43, 'מד': 44, 'מה': 45, 'מו': 46, 'מז': 47, 'מח': 48, 'מט': 49, 'נ': 50,
        'נא': 51, 'נב': 52, 'נג': 53, 'נד': 54, 'נה': 55, 'נו': 56, 'נז': 57, 'נח': 58, 'נט': 59, 'ס': 60,
        'סא': 61, 'סב': 62, 'סג': 63, 'סד': 64, 'סה': 65, 'סו': 66, 'סז': 67, 'סח': 68, 'סט': 69, 'ע': 70,
        'עא': 71, 'עב': 72, 'עג': 73, 'עד': 74, 'עה': 75, 'עו': 76, 'עז': 77, 'עח': 78, 'עט': 79, 'פ': 80,
        'פא': 81, 'פב': 82, 'פג': 83, 'פד': 84, 'פה': 85, 'פו': 86, 'פז': 87, 'פח': 88, 'פט': 89, 'צ': 90,
        'צא': 91, 'צב': 92, 'צג': 93, 'צד': 94, 'צה': 95, 'צו': 96, 'צז': 97, 'צח': 98, 'צט': 99, 'ק': 100,
        'קא': 101, 'קב': 102, 'קג': 103, 'קד': 104, 'קה': 105, 'קו': 106, 'קז': 107, 'קח': 108, 'קט': 109, 'קי': 110,
        'קיא': 111, 'קיב': 112, 'קיג': 113, 'קיד': 114, 'קטו': 115, 'קטז': 116, 'קיז': 117, 'קיח': 118, 'קיט': 119, 'קכ': 120,
        'קכא': 121, 'קכב': 122, 'קכג': 123, 'קכד': 124, 'קכה': 125, 'קכו': 126, 'קכז': 127, 'קכח': 128, 'קכט': 129, 'קל': 130,
        'קלא': 131, 'קלב': 132, 'קלג': 133, 'קלד': 134, 'קלה': 135, 'קלו': 136, 'קלז': 137, 'קלח': 138, 'קלט': 139, 'קמ': 140,
        'קמא': 141, 'קמב': 142, 'קמג': 143, 'קמד': 144, 'קמה': 145, 'קמו': 146, 'קמז': 147, 'קמח': 148, 'קמט': 149, 'קנ': 150,
        'קנא': 151, 'קנב': 152, 'קנג': 153, 'קנד': 154, 'קנה': 155, 'קנו': 156, 'קנז': 157, 'קנח': 158, 'קנט': 159, 'קס': 160,
        'קסא': 161, 'קסב': 162, 'קסג': 163, 'קסד': 164, 'קסה': 165, 'קסו': 166, 'קסז': 167, 'קסח': 168, 'קסט': 169, 'קע': 170,
        'קעא': 171, 'קעב': 172, 'קעג': 173, 'קעד': 174, 'קעה': 175, 'קעו': 176
    }
    
    page_num = hebrew_numbers.get(daf_hebrew, 0)
    # Convert to amud number (each daf has 2 amudim)
    # מ ע"א = 40a = (40-1)*2 + 1 = 79
    # מ ע"ב = 40b = (40-1)*2 + 2 = 80
    if amud == 'א':
        return (page_num - 1) * 2 + 1
    else:  # ב
        return (page_num - 1) * 2 + 2

def download_daf_page(massechet_num, amud_num):
    """Download a single daf page"""
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
    """Extract the Hebrew title and פירוש שטיינזלץ content"""
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
    
    # Clean up duplicate titles and unwanted elements in the content
    if steinsaltz_section:
        # Remove any h1 elements that duplicate the title
        for h1 in steinsaltz_section.find_all('h1'):
            h1.decompose()
        
        # Remove any h2 elements with "פירוש שטיינזלץ"
        for h2 in steinsaltz_section.find_all('h2'):
            if 'פירוש שטיינזלץ' in h2.get_text():
                h2.decompose()
        
        # Remove any heading elements that contain the exact title
        title_clean = title.replace('"', '').strip()
        for tag in steinsaltz_section.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            tag_text = tag.get_text().replace('"', '').strip()
            if title_clean in tag_text or tag_text in title_clean:
                tag.decompose()
        
        # Also check for div elements that might contain the title
        for div in steinsaltz_section.find_all('div'):
            div_text = div.get_text().strip()
            # Only remove if the div ONLY contains the title (not if it has other content)
            if len(div_text) < 50 and title_clean in div_text.replace('"', ''):
                div.decompose()
    
    return title, steinsaltz_section

def create_html_page(title, content, original_url):
    """Create a complete HTML page with the extracted content"""
    html_template = f"""<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Times New Roman', serif;
            direction: rtl;
            text-align: right;
            margin: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #8B4513;
            border-bottom: 2px solid #8B4513;
            padding-bottom: 10px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="content">
        {content}
    </div>
</body>
</html>"""
    return html_template

def download_daf_range(massechet_num, start_daf, start_amud, end_daf, end_amud):
    """Download a range of daf pages"""
    
    # Create output directory
    output_dir = 'pages'
    os.makedirs(output_dir, exist_ok=True)
    
    # Hebrew numbers for file naming
    hebrew_numbers = {
        2: 'ב', 3: 'ג', 4: 'ד', 5: 'ה', 6: 'ו', 7: 'ז', 8: 'ח', 9: 'ט', 10: 'י',
        11: 'יא', 12: 'יב', 13: 'יג', 14: 'יד', 15: 'טו', 16: 'טז', 17: 'יז', 18: 'יח', 19: 'יט', 20: 'כ',
        21: 'כא', 22: 'כב', 23: 'כג', 24: 'כד', 25: 'כה', 26: 'כו', 27: 'כז', 28: 'כח', 29: 'כט', 30: 'ל',
        31: 'לא', 32: 'לב', 33: 'לג', 34: 'לד', 35: 'לה', 36: 'לו', 37: 'לז', 38: 'לח', 39: 'לט', 40: 'מ',
        41: 'מא', 42: 'מב', 43: 'מג', 44: 'מד', 45: 'מה', 46: 'מו', 47: 'מז', 48: 'מח', 49: 'מט', 50: 'נ',
        51: 'נא', 52: 'נב', 53: 'נג', 54: 'נד', 55: 'נה', 56: 'נו', 57: 'נז', 58: 'נח', 59: 'נט', 60: 'ס',
        61: 'סא', 62: 'סב', 63: 'סג', 64: 'סד', 65: 'סה', 66: 'סו', 67: 'סז', 68: 'סח', 69: 'סט', 70: 'ע',
        71: 'עא', 72: 'עב', 73: 'עג', 74: 'עד', 75: 'עה', 76: 'עו', 77: 'עז', 78: 'עח', 79: 'עט', 80: 'פ',
        81: 'פא', 82: 'פב', 83: 'פג', 84: 'פד', 85: 'פה', 86: 'פו', 87: 'פז', 88: 'פח', 89: 'פט', 90: 'צ',
        91: 'צא', 92: 'צב', 93: 'צג', 94: 'צד', 95: 'צה', 96: 'צו', 97: 'צז', 98: 'צח', 99: 'צט', 100: 'ק',
        101: 'קא', 102: 'קב', 103: 'קג', 104: 'קד', 105: 'קה', 106: 'קו', 107: 'קז', 108: 'קח', 109: 'קט', 110: 'קי',
        111: 'קיא', 112: 'קיב', 113: 'קיג', 114: 'קיד', 115: 'קטו', 116: 'קטז', 117: 'קיז', 118: 'קיח', 119: 'קיט', 120: 'קכ',
        121: 'קכא', 122: 'קכב', 123: 'קכג', 124: 'קכד', 125: 'קכה', 126: 'קכו', 127: 'קכז', 128: 'קכח', 129: 'קכט', 130: 'קל',
        131: 'קלא', 132: 'קלב', 133: 'קלג', 134: 'קלד', 135: 'קלה', 136: 'קלו', 137: 'קלז', 138: 'קלח', 139: 'קלט', 140: 'קמ',
        141: 'קמא', 142: 'קמב', 143: 'קמג', 144: 'קמד', 145: 'קמה', 146: 'קמו', 147: 'קמז', 148: 'קמח', 149: 'קמט', 150: 'קנ',
        151: 'קנא', 152: 'קנב', 153: 'קנג', 154: 'קנד', 155: 'קנה', 156: 'קנו', 157: 'קנז', 158: 'קנח', 159: 'קנט', 160: 'קס',
        161: 'קסא', 162: 'קסב', 163: 'קסג', 164: 'קסד', 165: 'קסה', 166: 'קסו', 167: 'קסז', 168: 'קסח', 169: 'קסט', 170: 'קע',
        171: 'קעא', 172: 'קעב', 173: 'קעג', 174: 'קעד', 175: 'קעה', 176: 'קעו'
    }
    
    # Convert Hebrew daf numbers to numeric
    daf_mapping = {v: k for k, v in hebrew_numbers.items()}
    
    start_num = daf_mapping[start_daf]
    end_num = daf_mapping[end_daf]
    
    for daf_num in range(start_num, end_num + 1):
        for amud in ['א', 'ב']:
            # Skip if we're at start daf and before start amud
            if daf_num == start_num and start_amud == 'ב' and amud == 'א':
                continue
            # Skip if we're at end daf and after end amud  
            if daf_num == end_num and end_amud == 'א' and amud == 'ב':
                continue
                
            daf_hebrew = hebrew_numbers[daf_num]
            amud_number = hebrew_to_amud_number(daf_hebrew, amud)
            
            print(f"Downloading דף {daf_hebrew} עמוד {amud}...")
            
            # Download the page
            html_content = download_daf_page(massechet_num, amud_number)
            if html_content:
                # Extract title and content
                title, content = extract_content_and_title(html_content)
                
                if title and content:
                    # Create complete HTML page
                    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_number}&fs=0"
                    complete_html = create_html_page(title, str(content), url)
                    
                    # Clean filename
                    filename = f"{title.replace('\"', '').replace('/', '_')}.html"
                    filename = re.sub(r'[<>:"|?*]', '_', filename)
                    
                    # Save file
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(complete_html)
                    
                    print(f"✓ Saved: {filename}")
                else:
                    print(f"✗ Could not extract content for דף {daf_hebrew} עמוד {amud}")
            else:
                print(f"✗ Failed to download דף {daf_hebrew} עמוד {amud}")

if __name__ == "__main__":
    # Download עבודה זרה from דף מו עמוד א through דף נג עמוד ב
    massechet_avodah_zarah = 309
    
    print("Starting download of עבודה זרה דף מו עמוד א - נג עמוד ב...")
    download_daf_range(massechet_avodah_zarah, 'מו', 'א', 'נג', 'ב')
    print("Download completed!") 