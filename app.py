#!/usr/bin/env python3
"""
Daf Yomi Web Application
Flask web server for downloading and combining Daf Yomi pages
"""

from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import re
import tempfile
import zipfile
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Hebrew number mappings
HEBREW_NUMBERS = {
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
}

# Reverse mapping for converting numbers back to Hebrew
NUMBER_TO_HEBREW = {v: k for k, v in HEBREW_NUMBERS.items()}

# All tractates - exactly like your manual scripts would handle
TRACTATES = {
    'ברכות': 301,
    'שבת': 302, 
    'עירובין': 303,
    'פסחים': 304,
    'שקלים': 305,
    'יומא': 306,
    'סוכה': 307,
    'ביצה': 308,
    'עבודה זרה': 309,  # We have local files (סב-עו) as fallback
    'הוריות': 310,      # We have local files (ה-י) as fallback
    'זבחים': 311,       # We have local files (ב-ה) as fallback
    'ראש השנה': 312,
    'תענית': 313,
    'מגילה': 314,
    'מועד קטן': 315,
    'חגיגה': 316,
    'יבמות': 317,
    'כתובות': 318,
    'נדרים': 319,
    'נזיר': 320,
    'סוטה': 321,
    'גיטין': 322,
    'קידושין': 323,
    'בבא קמא': 324,
    'בבא מציעא': 325,
    'בבא בתרא': 326,
    'סנהדרין': 327,
    'מכות': 328,
    'שבועות': 329,
    'מנחות': 330,
    'חולין': 331,
    'בכורות': 332,
    'ערכין': 333,
    'תמורה': 334,
    'כריתות': 335,
    'מעילה': 336,
    'תמיד': 337,
    'מדות': 338,
    'קינים': 339,
    'נדה': 340
}

def hebrew_to_amud_number(daf_hebrew, amud):
    """Convert Hebrew daf notation to amud number used by the site"""
    page_num = HEBREW_NUMBERS.get(daf_hebrew, 0)
    if page_num == 0:
        return 0
    
    if amud == 'א':
        return (page_num - 1) * 2 + 1
    else:  # ב
        return (page_num - 1) * 2 + 2

def download_daf_page(massechet_num, amud_num):
    """Download a single daf page - EXACTLY like your manual scripts"""
    url = f"https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet={massechet_num}&amud={amud_num}&fs=0"
    
    # Use EXACT same headers as your working manual script
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
        
        # Try local files as fallback for tractates we have
        local_content = try_load_existing_page(massechet_num, amud_num)
        if local_content:
            print(f"Using local file as fallback")
            return local_content
        
        print(f"No local fallback available")
        return None

def try_load_existing_page(massechet_num, amud_num):
    """Try to load an existing downloaded page from the pages/ directory"""
    print(f"DEBUG: Looking for massechet_num={massechet_num}, amud_num={amud_num}")
    
    # Convert massechet number to name
    massechet_names = {v: k for k, v in TRACTATES.items()}
    massechet_name = massechet_names.get(massechet_num, "")
    print(f"DEBUG: massechet_name = '{massechet_name}'")
    
    if not massechet_name:
        print(f"DEBUG: No massechet name found for ID {massechet_num}")
        return None
        
    # Convert amud number back to daf and side
    # amud_num = (page_num - 1) * 2 + 1 for א, (page_num - 1) * 2 + 2 for ב
    # So: page_num = (amud_num + 1) // 2 for א, (amud_num) // 2 + 1 for ב
    if amud_num % 2 == 1:  # א
        daf_num = (amud_num + 1) // 2
        side = 'א'
    else:  # ב
        daf_num = amud_num // 2
        side = 'ב'
    
    daf_hebrew = NUMBER_TO_HEBREW.get(daf_num, str(daf_num))
    print(f"DEBUG: amud_num={amud_num} -> daf_num={daf_num} -> daf_hebrew='{daf_hebrew}' side='{side}'")
    
    # Try to find the file in pages/ directory
    import glob
    pages_dir = "pages"
    
    # Look for files matching the pattern
    possible_patterns = [
        f"{massechet_name} {daf_hebrew} ע{side}.html",
        f"{massechet_name} {daf_hebrew} ע\"{side}\".html", 
        f"{massechet_name}_{daf_hebrew}_ע{side}.html"
    ]
    
    print(f"DEBUG: Looking for patterns: {possible_patterns}")
    
    for pattern in possible_patterns:
        file_path = os.path.join(pages_dir, pattern)
        print(f"DEBUG: Checking {file_path}")
        if os.path.exists(file_path):
            print(f"Found existing file: {file_path}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                continue
    
    print(f"No existing file found for {massechet_name} {daf_hebrew} ע{side}")
    
    # List what files are actually there
    if os.path.exists(pages_dir):
        actual_files = [f for f in os.listdir(pages_dir) if massechet_name in f and f.endswith('.html')]
        print(f"DEBUG: Actual files containing '{massechet_name}': {actual_files}")
    
    return None


def extract_content_and_title(html_content):
    """Extract the Hebrew title and content - works with both raw and processed pages"""
    if not html_content:
        return None, None
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract Hebrew title
    title_element = soup.find('h1')
    if title_element:
        title = title_element.get_text().strip()
    else:
        # Try title tag as fallback
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else "Unknown"
    
    # For already processed files (from pages/ directory), just get the body content
    content_div = soup.find('div', class_='content')
    if content_div:
        print("DEBUG: Found .content div in processed file")
        return title, content_div
    
    # For raw files from daf-yomi.com, look for פירוש שטיינזלץ section
    steinsaltz_heading = soup.find('h2', string=lambda text: text and 'פירוש שטיינזלץ' in text)
    if steinsaltz_heading:
        print("DEBUG: Found פירוש שטיינזלץ section in raw file")
        steinsaltz_section = steinsaltz_heading.find_parent()
        if steinsaltz_section:
            content_div = steinsaltz_section.find('div')
            if content_div:
                steinsaltz_section = content_div
        
        # Clean up content
        if steinsaltz_section:
            for h1 in steinsaltz_section.find_all('h1'):
                h1.decompose()
            for h2 in steinsaltz_section.find_all('h2'):
                if 'פירוש שטיינזלץ' in h2.get_text():
                    h2.decompose()
        
        return title, steinsaltz_section
    
    # Fallback: for processed files, just get the body content minus the h1
    body = soup.find('body')
    if body:
        print("DEBUG: Using body content as fallback")
        # Create a copy and remove the h1 to avoid duplication
        body_copy = BeautifulSoup(str(body), 'html.parser')
        title_in_body = body_copy.find('h1')
        if title_in_body:
            title_in_body.decompose()
        return title, body_copy
    
    print("DEBUG: No content found")
    return title, None

def create_html_page(title, content):
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

@app.route('/')
def index():
    """Main page with form for selecting tractate and pages"""
    return render_template('index.html', tractates=TRACTATES)

@app.route('/api/download', methods=['POST'])
def download_pages():
    """API endpoint to download and combine pages"""
    try:
        print(f"DEBUG: Received download request")
        data = request.json
        print(f"DEBUG: Request data: {data}")
        
        tractate_name = data.get('tractate')
        start_daf = data.get('start_daf')
        start_amud = data.get('start_amud')
        end_daf = data.get('end_daf')  
        end_amud = data.get('end_amud')
        
        print(f"DEBUG: tractate='{tractate_name}', start='{start_daf}{start_amud}', end='{end_daf}{end_amud}'")
        
        # Validate inputs
        if not all([tractate_name, start_daf, start_amud, end_daf, end_amud]):
            print(f"DEBUG: Missing parameters")
            return jsonify({'error': 'Missing required parameters'}), 400
            
        # Get tractate ID
        massechet_num = TRACTATES.get(tractate_name)
        print(f"DEBUG: Found massechet_num={massechet_num} for '{tractate_name}'")
        if not massechet_num:
            return jsonify({'error': f'Unknown tractate: {tractate_name}'}), 400
            
        # Validate Hebrew page numbers
        if start_daf not in HEBREW_NUMBERS or end_daf not in HEBREW_NUMBERS:
            return jsonify({'error': 'Invalid Hebrew page numbers'}), 400
            
        # Create temporary directory for pages
        with tempfile.TemporaryDirectory() as temp_dir:
            pages = []
            
            start_num = HEBREW_NUMBERS[start_daf]
            end_num = HEBREW_NUMBERS[end_daf]
            
            # Download pages
            for daf_num in range(start_num, end_num + 1):
                for amud in ['א', 'ב']:
                    # Skip if we're at start daf and before start amud
                    if daf_num == start_num and start_amud == 'ב' and amud == 'א':
                        continue
                    # Skip if we're at end daf and after end amud  
                    if daf_num == end_num and end_amud == 'א' and amud == 'ב':
                        continue
                        
                    daf_hebrew = NUMBER_TO_HEBREW[daf_num]
                    amud_number = hebrew_to_amud_number(daf_hebrew, amud)
                    
                    if amud_number == 0:
                        continue
                        
                    # Download the page
                    print(f"DEBUG: Downloading {daf_hebrew} {amud} (amud_number={amud_number})")
                    html_content = download_daf_page(massechet_num, amud_number)
                    print(f"DEBUG: html_content length: {len(html_content) if html_content else 0}")
                    
                    if html_content:
                        title, content = extract_content_and_title(html_content)
                        print(f"DEBUG: title='{title[:50] if title else None}...', content={'Yes' if content else 'No'}")
                        
                        if title and content:
                            complete_html = create_html_page(title, str(content))
                            pages.append({'title': title, 'content': complete_html})
                            print(f"DEBUG: Added page to list, total pages: {len(pages)}")
                        else:
                            print(f"DEBUG: Failed to extract title/content from page")
                    else:
                        print(f"DEBUG: No html_content for {daf_hebrew} {amud}")
            
            print(f"DEBUG: Final pages count: {len(pages)}")
            if not pages:
                error_msg = f'Unable to download {tractate_name} pages. The daf-yomi.com site appears to be blocking automated requests (likely Cloudflare protection). This affects both the web app and manual scripts. You may need to: 1) Try from a different network, 2) Use a VPN, or 3) Wait for the site restrictions to be lifted.'
                return jsonify({'error': error_msg}), 404
                
            # Create combined HTML
            combined_html = create_combined_html(pages, tractate_name, start_daf, start_amud, end_daf, end_amud)
            
            # Save to temporary file
            filename = f"{tractate_name}_{start_daf}{start_amud}-{end_daf}{end_amud}.html"
            temp_file = os.path.join(temp_dir, filename)
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(combined_html)
                
            return send_file(temp_file, as_attachment=True, download_name=filename)
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def create_combined_html(pages, tractate_name, start_daf, start_amud, end_daf, end_amud):
    """Create combined HTML from multiple pages"""
    title = f"{tractate_name} {start_daf} {start_amud} - {end_daf} {end_amud}"
    
    html = f"""<!DOCTYPE html>
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
        .page {{
            page-break-after: always;
            margin-bottom: 30px;
            border-bottom: 2px dashed #ccc;
            padding-bottom: 20px;
        }}
        h1 {{
            color: #8B4513;
            border-bottom: 2px solid #8B4513;  
            padding-bottom: 10px;
            text-align: center;
        }}
        .page h1 {{
            text-align: right;
            font-size: 1.5em;
            margin-bottom: 15px;
        }}
        @media print {{
            .page {{
                page-break-after: always;
                border-bottom: none;
            }}
        }}
    </style>
</head>
<body>
    <h1>📖 {title}</h1>
"""
    
    for page in pages:
        soup = BeautifulSoup(page['content'], 'html.parser')
        
        # Extract title and content properly
        page_title = soup.find('h1')
        page_content = soup.find('body')
        
        html += f'<div class="page">\n'
        
        if page_title:
            html += f'<h1>{page_title.get_text().strip()}</h1>\n'
            
        if page_content:
            # Remove the h1 from content to avoid duplication
            content_copy = BeautifulSoup(str(page_content), 'html.parser')
            title_in_content = content_copy.find('h1')
            if title_in_content:
                title_in_content.decompose()
            
            html += str(content_copy.get_text() if content_copy else "")
            
        html += '</div>\n\n'
    
    html += """</body>
</html>"""
    
    return html

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)