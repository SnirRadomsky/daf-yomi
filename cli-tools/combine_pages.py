import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Directory containing the HTML files
pages_dir = Path("pages")

# Output file path
output_file = Path("combined_pages.html")

# Hebrew to number mapping for sorting
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

def get_sorting_key(filename):
    """Extract tractate, page number and side for sorting Hebrew filenames"""
    # Pattern for Hebrew filenames like "עבודה זרה יא עב.html"
    match = re.search(r'(.+?)\s+([^\s]+)\s+(עא|עב)\.html$', filename)
    if match:
        tractate, page_hebrew, side = match.groups()
        page_num = hebrew_numbers.get(page_hebrew, 0)
        side_num = 1 if side == 'עא' else 2
        return (tractate, page_num, side_num)
    return (filename, 0, 0)

# Get all HTML files
html_files = [f for f in os.listdir(pages_dir) if f.endswith(".html")]

# Sort files by tractate, page number, and side
html_files.sort(key=get_sorting_key)

# Create the combined HTML file with RTL support
with open(output_file, "w", encoding="utf-8") as out_file:
    # Write HTML header with RTL direction
    out_file.write("""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Daf Yomi Pages</title>
    <style>
        body {
            direction: rtl;
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            margin: 20px;
            text-align: right;
        }
        .page {
            page-break-after: always;
            margin-bottom: 30px;
            border-bottom: 2px dashed #ccc;
            padding-bottom: 20px;
        }
        h1 {
            color: #8B4513;
            border-bottom: 2px solid #8B4513;
            padding-bottom: 10px;
            text-align: center;
            font-size: 28px;
        }
        big {
            font-size: 1.5em;
            font-weight: bold;
        }
        small {
            font-size: 0.8em;
            color: #666;
        }
        @media print {
            .page {
                page-break-after: always;
                border-bottom: none;
            }
        }
    </style>
</head>
<body>
""")

    # Process each file and append to the combined document
    for i, filename in enumerate(html_files):
        # Read and parse the HTML file
        with open(pages_dir / filename, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Parse HTML to extract body content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract the h1 title and the content div
        h1_tag = soup.find('h1')
        content_div = soup.find('div', class_='content')
        
        # Write page with content
        out_file.write(f'<div class="page">\n')
        
        # Write the h1 if found
        if h1_tag:
            out_file.write(str(h1_tag) + '\n')
        
        # Write the content
        if content_div:
            out_file.write(str(content_div) + '\n')
        else:
            # Fallback: write the entire body content if no content div found
            body = soup.find('body')
            if body:
                out_file.write(''.join(str(child) for child in body.children))
        
        out_file.write('</div>\n\n')
    
    # Close the HTML document
    out_file.write("""</body>
</html>
""")

print(f"Successfully combined {len(html_files)} files into {output_file}")
print(f"Files processed in order: {', '.join(html_files)}") 