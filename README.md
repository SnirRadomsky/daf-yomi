# Daf Yomi Tools 📜

A collection of Python tools for downloading, organizing, and formatting Hebrew Talmud pages for study and printing. Perfect for Daf Yomi learners who want to combine multiple pages into a single, printer-friendly document.

## 🎯 Features

- **Download Daf Yomi Content**: Fetch Hebrew Talmud pages directly from daf-yomi.com
- **Smart Page Combination**: Merge multiple HTML pages with proper Hebrew (RTL) formatting
- **Intelligent Sorting**: Automatically sorts pages by tractate, page number, and side (A/B)
- **Print-Optimized**: Creates printer-friendly documents with proper page breaks
- **Hebrew Number Support**: Full Hebrew numeral system support (ב to קע)
- **Tractate-Specific Tools**: Specialized combiners for different tractates

## 📁 Project Structure

```
daf-yomi/
├── README.md                    # This file
├── README_download.md           # Download instructions
├── download_daf_simple.py       # Main download script
├── combine_pages.py             # General page combiner
├── combine_pages_with_titles.py # Enhanced combiner with titles
├── combine_avodah_zarah.py      # Avodah Zarah specific combiner
├── combined_pages.html          # Output file (generated)
└── pages/                       # Directory for downloaded HTML files
```

## 🚀 Quick Start

### 1. Download Daf Yomi Content

```bash
python download_daf_simple.py
```

This script will:
- Download Hebrew Talmud pages from daf-yomi.com
- Save them as HTML files in the `pages` directory
- Handle Hebrew numeral conversion automatically

### 2. Combine Pages for Printing

```bash
python combine_pages.py
```

This will:
- Read all HTML files from the `pages` directory
- Sort them intelligently by tractate and page number
- Create a single `combined_pages.html` file
- Format with proper RTL direction for Hebrew text
- Add page breaks for clean printing

### 3. Print Your Study Materials

1. Open `combined_pages.html` in your web browser
2. Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (Mac)
3. Adjust print settings as needed
4. Print your combined Daf Yomi pages!

## 🛠️ Available Scripts

### `download_daf_simple.py`
Downloads content directly from daf-yomi.com using HTTP requests.

**Features:**
- Hebrew numeral to number conversion
- Automatic file naming
- Error handling for failed downloads
- Support for different tractates

### `combine_pages.py`
Basic page combiner with essential features.

**Features:**
- Automatic sorting by page order
- RTL text direction support
- Print-optimized CSS
- Page break insertion

### `combine_pages_with_titles.py`
Enhanced combiner with additional title formatting.

**Features:**
- All features of basic combiner
- Enhanced page titles
- Better visual separation
- Improved readability

### `combine_avodah_zarah.py`
Specialized combiner for Avodah Zarah tractate.

**Features:**
- Tractate-specific optimizations
- Custom sorting logic
- Specialized formatting

## 📋 Requirements

- **Python 3.6+**
- **Required packages:**
  ```bash
  pip install requests beautifulsoup4
  ```

## 🔧 Configuration

### Hebrew Number Support
The scripts include comprehensive Hebrew numeral mapping:
- ב (2) through קע (170)
- Handles complex combinations like קיג (113), קכד (124)
- Automatic conversion for daf-yomi.com URL format

### File Organization
- Downloaded files are saved in the `pages/` directory
- Output files are created in the project root
- HTML files are automatically sorted by name

## 💡 Usage Examples

### Download Specific Pages
```python
# Modify download_daf_simple.py to download specific ranges
# Example: Download Berakhot pages 2-10
```

### Custom Combination
```python
# Use combine_pages.py for general combination
# Use combine_pages_with_titles.py for enhanced formatting
# Use combine_avodah_zarah.py for Avodah Zarah specific pages
```

### Print Settings
For best results when printing:
- Use A4 or Letter paper size
- Enable background graphics
- Set margins to 0.5 inches
- Consider landscape orientation for wider pages

## 🌐 Hebrew Text Support

This project is optimized for Hebrew Talmud text:
- **RTL (Right-to-Left) text direction**
- **Hebrew numeral system support**
- **Proper Unicode handling**
- **Print-friendly Hebrew formatting**

## 📖 Daf Yomi Background

Daf Yomi (דף יומי, "daily page") is a daily regimen of learning the Talmud, where participants study one page per day, completing the entire Talmud in approximately 7.5 years. This project helps learners:

- Download and organize daily study materials
- Create printer-friendly study packets
- Combine multiple days for review sessions
- Maintain proper Hebrew text formatting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Hebrew text
5. Submit a pull request

## 📄 License

This project is for educational and religious study purposes. Please respect copyright and terms of use for source materials.

## 🆘 Troubleshooting

### Common Issues:

**Download failures:**
- Check internet connection
- Verify daf-yomi.com is accessible
- Ensure proper Hebrew encoding

**Combination issues:**
- Verify HTML files are in `pages/` directory
- Check file naming conventions
- Ensure proper Hebrew text encoding

**Printing problems:**
- Enable background graphics in browser
- Use recent browser version
- Check RTL text support

## 🙏 Acknowledgments

- daf-yomi.com for providing accessible Talmud content
- The global Daf Yomi learning community
- Contributors to Hebrew text processing tools

---

*Happy Learning! חזק ואמץ*
