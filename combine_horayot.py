import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Output file path
output_file = Path("horayot_5-9.html")

# Hebrew to number mapping for sorting
hebrew_numbers = {
    'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'יא': 11, 'יב': 12, 'יג': 13, 'יד': 14, 'טו': 15, 'טז': 16, 'יז': 17, 'יח': 18, 'יט': 19, 'כ': 20,
    'כא': 21, 'כב': 22, 'כג': 23, 'כד': 24, 'כה': 25, 'כו': 26, 'כז': 27, 'כח': 28, 'כט': 29, 'ל': 30,
    'לא': 31, 'לב': 32, 'לג': 33, 'לד': 34, 'לה': 35, 'לו': 36, 'לז': 37, 'לח': 38, 'לט': 39, 'מ': 40,
    'מא': 41, 'מב': 42, 'מג': 43, 'מד': 44, 'מה': 45, 'מו': 46, 'מז': 47, 'מח': 48, 'מט': 49, 'נ': 50,
    'נא': 51, 'נב': 52, 'נג': 53, 'נד': 54, 'נה': 55, 'נו': 56, 'נז': 57, 'נח': 58, 'נט': 59, 'ס': 60,
    'סא': 61, 'סב': 62, 'סג': 63, 'סד': 64, 'סה': 65, 'סו': 66, 'סז': 67, 'סח': 68, 'סט': 69, 'ע': 70,
    'עא': 71, 'עב': 72, 'עג': 73, 'עד': 74, 'עה': 75, 'עו': 76, 'עז': 77, 'עח': 78, 'עט': 79, 'פ': 80
}

def get_sorting_key(filename):
    """Extract tractate, page number and side for sorting Hebrew filenames"""
    # Pattern for Hebrew filenames like "הוריות ה עב.html"
    match = re.search(r'(.+?)\s+([^\s]+)\s+(עא|עב)\.html$', filename)
    if match:
        tractate, page_hebrew, side = match.groups()
        page_num = hebrew_numbers.get(page_hebrew, 0)
        side_num = 1 if side == 'עא' else 2
        return (tractate, page_num, side_num)
    return (filename, 0, 0)

# Define the range we want to include
start_daf = 'ה'
start_amud = 'ב'
end_daf = 'ט'
end_amud = 'ב'

# Get all HTML files in the pages directory
pages_dir = Path("pages")
all_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]

# Filter files to include only those in our range
filtered_files = []
for filename in all_files:
    if not filename.startswith('הוריות'):
        continue
    
    match = re.search(r'הוריות\s+([^\s]+)\s+(עא|עב)\.html$', filename)
    if not match:
        continue
    
    daf, amud = match.groups()
    
    # Check if this file is within our range
    if hebrew_numbers.get(daf, 0) > hebrew_numbers.get(start_daf, 0) or \
       (hebrew_numbers.get(daf, 0) == hebrew_numbers.get(start_daf, 0) and 
        (amud == 'עא' and start_amud == 'א' or amud == 'עב' and start_amud in ['א', 'ב'])):
        if hebrew_numbers.get(daf, 0) < hebrew_numbers.get(end_daf, 0) or \
           (hebrew_numbers.get(daf, 0) == hebrew_numbers.get(end_daf, 0) and 
            (amud == 'עא' and end_amud in ['א', 'ב'] or amud == 'עב' and end_amud == 'ב')):
            filtered_files.append(filename)

# Sort files by tractate, page number, and side
filtered_files.sort(key=get_sorting_key)

# Create combined HTML
with open(output_file, 'w', encoding='utf-8') as outfile:
    outfile.write("""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>הוריות דף ה עמוד ב - דף ט עמוד ב</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
            color: #333;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .main-title {
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
            font-weight: bold;
        }
        
        .page-marker {
            font-size: 16px;
            font-weight: bold;
            display: inline-block;
            background-color: #f0f0f0;
            padding: 3px 8px;
            margin: 10px 0 5px 0;
            border-radius: 4px;
            border: 1px solid #ddd;
        }
        
        .page-content {
            margin: 0 0 10px 0;
        }
        
        .separator {
            border-top: 1px dashed #ccc;
            margin: 5px 0;
        }
        
        p {
            margin-top: 5px;
            margin-bottom: 5px;
        }
        
        @media print {
            body {
                max-width: 100%;
            }
            
            .page-break {
                page-break-before: always;
            }
        }
    </style>
</head>
<body>
<h1 class="main-title">הוריות דף ה עמוד ב - דף ט עמוד ב</h1>
""")

    for i, filename in enumerate(filtered_files):
        file_path = pages_dir / filename
        
        with open(file_path, 'r', encoding='utf-8') as infile:
            soup = BeautifulSoup(infile.read(), 'html.parser')
            
            # Extract title and content
            title = soup.find('h1')
            content_div = soup.find('div', class_='content')
            
            if title and content_div:
                # Add page break class for print view (every two pages)
                page_break_class = ' page-break' if i > 0 and i % 2 == 0 else ''
                
                # Extract title text
                title_text = title.get_text().strip()
                
                # Write page title
                outfile.write(f'<div class="page-marker{page_break_class}">{title_text}</div>\n')
                
                # Process content to clean up internal headings
                content_html = str(content_div)
                
                # Convert internal h1, h2, h3 tags to <strong> wrapped in <p>
                content_html = re.sub(r'<h[123][^>]*>(.*?)</h[123]>', r'<p><strong>\1</strong></p>', content_html)
                
                # Clean up nested divs
                content_html = re.sub(r'<div[^>]*>(.*?)</div>', r'<span>\1</span>', content_html)
                
                # Write processed content
                outfile.write(f'<div class="page-content">{content_html}</div>\n')
                
                # Add separator between pages
                if i < len(filtered_files) - 1:
                    outfile.write('<div class="separator"></div>\n')
    
    outfile.write("</body>\n</html>")

# Report success
print(f"Successfully combined {len(filtered_files)} files into {output_file}")
print(f"Files processed in order: {', '.join(filtered_files)}")