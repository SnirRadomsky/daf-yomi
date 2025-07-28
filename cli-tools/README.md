# CLI Tools

Legacy command-line tools for Daf Yomi page downloading and combining.

> **Note**: For the best experience, use the web application instead by running `./launch.sh` from the main directory.

## Available Scripts

- `download_daf_simple.py` - Download pages directly from daf-yomi.com
- `combine_pages.py` - Basic page combiner 
- `combine_pages_with_titles.py` - Enhanced combiner with titles
- `combine_avodah_zarah.py` - Avodah Zarah specific combiner

## Requirements

```bash
pip install requests beautifulsoup4
```

## Usage

```bash
cd cli-tools
python download_daf_simple.py
python combine_pages.py
```