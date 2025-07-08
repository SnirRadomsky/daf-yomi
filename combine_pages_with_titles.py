import os
import re
from pathlib import Path

# Directory containing the HTML files
pages_dir = Path("pages")

# Output file path
output_file = Path("combined_pages.html")

# Regular expression to extract tractate, page and side for sorting
pattern = re.compile(r"ShtainzaltzHebrew_([^_]+)_(\d+)([AB])\.html")

def get_sorting_key(filename):
    match = pattern.match(filename)
    if match:
        tractate, page_num, side = match.groups()
        # Pad page number with zeros for proper sorting
        return (tractate, int(page_num), side)
    return (filename, 0, "")

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
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
        }
        .page {
            page-break-after: always;
            margin-bottom: 30px;
            border-bottom: 1px dashed #ccc;
            padding-bottom: 20px;
        }
        .page-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            text-align: center;
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
            }
        }
    </style>
</head>
<body>
""")

    # Process each file and append to the combined document
    for i, filename in enumerate(html_files):
        # Extract page information for title
        match = pattern.match(filename)
        if match:
            tractate, page_num, side = match.groups()
            page_title = f"{tractate} {page_num}{side}"
        else:
            page_title = filename.replace("ShtainzaltzHebrew_", "").replace(".html", "")
        
        # Read the content of the file
        with open(pages_dir / filename, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Write page title and content
        out_file.write(f'<div class="page">\n')
        out_file.write(f'<div class="page-title">{page_title}</div>\n')
        out_file.write(f'{content}\n')
        out_file.write('</div>\n\n')
    
    # Close the HTML document
    out_file.write("""</body>
</html>
""")

print(f"Successfully combined {len(html_files)} files into {output_file}") 