# Daf Yomi Tools 📜

A collection of Python tools for downloading, organizing, and formatting Hebrew Talmud pages for study and printing. Includes both command-line scripts and a modern web application with real-time progress tracking. Perfect for Daf Yomi learners who want to combine multiple pages into a single, printer-friendly document.

## 🎯 Features

### Web Application (New!)
- 🌐 **Modern Web Interface**: Easy-to-use Hebrew RTL web interface
- 📊 **Real-time Progress Bar**: See download progress and current page being processed
- 🔍 **Searchable Tractate Selection**: Type to search tractates (e.g., "ירו" finds "עירובין")
- 📁 **Informative Filenames**: Downloads have meaningful names like `avodah_zarah_71-76.html`
- ⌨️ **Keyboard Navigation**: Use arrow keys to increment/decrement page numbers
- ⚡ **One-Click Launch**: `./launch.sh` starts server and opens browser automatically

### Command Line Tools
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
├── launch.sh                    # Web app launcher script ⚡
├── app.py                       # Flask web application 🌐
├── requirements.txt             # Python dependencies
├── templates/
│   └── index.html              # Web interface with Hebrew RTL support
├── cli-tools/                  # Legacy command-line tools
│   ├── README.md               # CLI tools documentation
│   ├── download_daf_simple.py  # CLI download script
│   ├── combine_pages.py        # General page combiner
│   ├── combine_pages_with_titles.py # Enhanced combiner
│   └── combine_avodah_zarah.py # Avodah Zarah specific combiner
└── pages/                      # Downloaded HTML files (git-ignored)
```

## 🚀 Quick Start

### Option 1: Web Application (Recommended)

**Launch the web app:**
```bash
./launch.sh
```

This will:
- Start the Flask web server automatically
- Open your browser to http://localhost:5001
- Provide a modern interface for downloading Daf Yomi pages

**Using the web interface:**
1. **Select Tractate**: Type to search (e.g., "בבא" shows all בבא tractates)
2. **Choose Page Range**: Use default ב עמוד א עד ב עמוד ב or customize with arrows
3. **Download**: Click "הורד דפים" and watch the real-time progress bar
4. **Get File**: Downloads automatically when complete with informative filenames

### Option 2: Command Line Tools (Legacy)

See `cli-tools/README.md` for documentation on the original command-line scripts.

## 🛠️ Web Application Components

### `app.py`
Flask web server with real-time progress tracking and Hebrew interface.

**Features:**
- Server-Sent Events for progress updates
- Hebrew number conversion system
- Informative filename generation
- Automatic file cleanup

### `templates/index.html`
Modern Hebrew RTL web interface.

**Features:**
- Searchable tractate selection
- Keyboard navigation support
- Real-time progress visualization
- Responsive design

### `launch.sh`
One-click launcher script for the web application.

**Features:**
- Automatic dependency checking
- Port conflict resolution
- Cross-platform browser opening

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
