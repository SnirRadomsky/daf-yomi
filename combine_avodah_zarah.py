import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Directory containing the HTML files
pages_dir = Path("pages")

# Output file path
output_file = Path("avodah_zarah_46-53.html")

# Hebrew to number mapping for sorting
hebrew_numbers = {
    'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'יא': 11, 'יב': 12, 'יג': 13, 'יד': 14, 'טו': 15, 'טז': 16, 'יז': 17, 'יח': 18, 'יט': 19, 'כ': 20,
    'כא': 21, 'כב': 22, 'כג': 23, 'כד': 24, 'כה': 25, 'כו': 26, 'כז': 27, 'כח': 28, 'כט': 29, 'ל': 30,
    'לא': 31, 'לב': 32, 'לג': 33, 'לד': 34, 'לה': 35, 'לו': 36, 'לז': 37, 'לח': 38, 'לט': 39, 'מ': 40,
    'מא': 41, 'מב': 42, 'מג': 43, 'מד': 44, 'מה': 45, 'מו': 46, 'מז': 47, 'מח': 48, 'מט': 49, 'נ': 50,
    'נא': 51, 'נב': 52, 'נג': 53, 'נד': 54, 'נה': 55, 'נו': 56, 'נז': 57, 'נח': 58, 'נט': 59, 'ס': 60
}

def get_sorting_key(filename):
    """Extract tractate, page number and side for sorting Hebrew filenames"""
    # Pattern for Hebrew filenames like "עבודה זרה מו עא.html"
    match = re.search(r'(.+?)\s+([^\s]+)\s+(עא|עב)\.html$', filename)
    if match:
        tractate, page_hebrew, side = match.groups()
        page_num = hebrew_numbers.get(page_hebrew, 0)
        side_num = 1 if side == 'עא' else 2
        return (tractate, page_num, side_num)
    return (filename, 0, 0)

# Define the range we want to include
start_daf = 'מו'
start_amud = 'א'
end_daf = 'נג'
end_amud = 'ב'

# Get all HTML files
all_files = [f for f in os.listdir(pages_dir) if f.endswith(".html")]
filtered_files = []

# Filter files to include only the desired range
for filename in all_files:
    match = re.search(r'עבודה זרה\s+([^\s]+)\s+(עא|עב)\.html$', filename)
    if match:
        daf_hebrew, amud = match.groups()
        daf_num = hebrew_numbers.get(daf_hebrew, 0)
        start_num = hebrew_numbers.get(start_daf, 0)
        end_num = hebrew_numbers.get(end_daf, 0)
        
        # Check if file is within range
        if start_num <= daf_num <= end_num:
            # Check for edge cases at start and end
            if daf_num == start_num and amud == 'עא' and start_amud == 'ב':
                continue
            if daf_num == end_num and amud == 'עב' and end_amud == 'א':
                continue
            filtered_files.append(filename)

# Sort files by tractate, page number, and side
filtered_files.sort(key=get_sorting_key)

# Create the combined HTML file with RTL support
with open(output_file, "w", encoding="utf-8") as out_file:
    # Write HTML header with RTL direction
    out_file.write("""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>עבודה זרה דף מו עמוד א - דף נג עמוד ב</title>
    <style>
        body {
            direction: rtl;
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 20px;
            text-align: right;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        .page-marker {
            color: #8B4513;
            font-weight: bold;
            font-size: 16px;
            display: inline-block;
            background-color: #f8f8f8;
            padding: 2px 8px;
            border-radius: 4px;
            margin-top: 10px;
            margin-bottom: 5px;
            border-bottom: 1px solid #ddd;
        }
        .main-title {
            color: #8B4513;
            border-bottom: 2px solid #8B4513;
            padding-bottom: 10px;
            text-align: center;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .page-content {
            margin-bottom: 10px;
        }
        .page-content p {
            margin-top: 0.5em;
            margin-bottom: 0.5em;
        }
        .separator {
            border-top: 1px dashed #ccc;
            margin: 5px 0;
        }
        @media print {
            .page-break {
                page-break-before: always;
            }
            body {
                max-width: 100%;
            }
        }
    </style>
</head>
<body>
<h1 class="main-title">עבודה זרה דף מו עמוד א - דף נג עמוד ב</h1>
""")

    # Process each file and append to the combined document
    for i, filename in enumerate(filtered_files):
        # Read and parse the HTML file
        with open(pages_dir / filename, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Parse HTML to extract body content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract the h1 title and the content div
        h1_tag = soup.find('h1')
        content_div = soup.find('div', class_='content')
        
        # Add page break class for print only on certain pages (every 2 pages)
        page_break_class = ' page-break' if i > 0 and i % 2 == 0 else ''
        
        # Write page title as a compact marker
        if h1_tag:
            title_text = h1_tag.get_text()
            out_file.write(f'<div class="page-marker{page_break_class}">{title_text}</div>\n')
        
        # Write the content
        out_file.write('<div class="page-content">\n')
        if content_div:
            # Remove any internal h1, h2 tags to save space
            for tag in content_div.find_all(['h1', 'h2', 'h3']):
                tag.name = 'strong'
                tag.wrap(soup.new_tag('p'))
            
            # Clean up any nested divs that might cause extra spacing
            for div in content_div.find_all('div'):
                div.name = 'span'
            
            out_file.write(str(content_div) + '\n')
        else:
            # Fallback: write the entire body content if no content div found
            body = soup.find('body')
            if body:
                for tag in body.find_all(['h1', 'h2', 'h3']):
                    tag.name = 'strong'
                    tag.wrap(soup.new_tag('p'))
                
                for div in body.find_all('div'):
                    if not div.get('class') or 'content' not in div.get('class'):
                        div.name = 'span'
                
                out_file.write(''.join(str(child) for child in body.children))
        
        out_file.write('</div>\n\n')
        
        # Add a subtle separator between pages except for the last page
        if i < len(filtered_files) - 1:
            out_file.write('<div class="separator"></div>\n\n')
    
    # Close the HTML document
    out_file.write("""</body>
</html>
""")

print(f"Successfully combined {len(filtered_files)} files into {output_file}")
print(f"Files processed in order: {', '.join(filtered_files)}") 