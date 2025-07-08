# Daf Yomi Page Combiner

This program combines multiple Hebrew Talmud HTML pages into a single document with proper right-to-left (RTL) text direction for easy printing.

## Usage

1. Make sure all your HTML files are in the `pages` directory
2. Run the script using Python:

```bash
python combine_pages.py
```

3. The script will create a file called `combined_pages.html` in the same directory
4. Open this file in your browser and print it (Ctrl+P or Cmd+P)

## Features

- Automatically sorts pages by tractate name, page number, and side (A/B)
- Sets proper RTL direction for Hebrew text
- Creates page breaks for each page when printing
- Adds page titles for better navigation

## Requirements

- Python 3.6 or higher 