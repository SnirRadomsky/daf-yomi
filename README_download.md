# Daf Yomi Content Downloader

This script downloads Daf Yomi content from [daf-yomi.com](https://daf-yomi.com) with Hebrew titles and extracts the פירוש שטיינזלץ content.

## Features

- Downloads content directly via HTTP (no browser automation needed)
- Extracts Hebrew titles like "שבועות מ ע\"א"
- Focuses on פירוש שטיינזלץ content specifically
- Creates clean HTML files with RTL Hebrew formatting
- Handles Hebrew daf notation (מ, מא, מב, מג, etc.)

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install requests beautifulsoup4
```

## Usage

### Basic Usage
```python
# Download שבועות from דף מ through דף מג
from download_daf_simple import download_daf_range

massechet_shevuot = 308
download_daf_range(massechet_shevuot, 'מ', 'א', 'מג', 'ב')
```

### Massechet Numbers

**Important:** The daf-yomi.com site uses its own numbering system, not the standard Talmudic order. Here are the confirmed massechet numbers:

```python
# Confirmed massechet numbers from daf-yomi.com
massechet_numbers = {
    'ברכות': 283,
    'שבת': 284,
    'פסחים': 286,
    'שבועות': 308,
    'עבודה זרה': 309,
    # Add more as you discover them...
}

# Note: Some massechtot have high daf numbers (up to 176):
# - בבא בתרא: up to דף קעו (176)
# - סנהדרין: up to דף קיג (113) 
# - חולין: up to דף קמב (142)
# Extended support now available for all dafim up to קעו (176)
```

**To find other massechet numbers:**
1. Go to [daf-yomi.com](https://daf-yomi.com/Dafyomi_Page.aspx?vt=5&massechet=308&amud=79&fs=0)
2. Select the desired massechet from the dropdown
3. Click "הצגה" (Display)
4. Check the URL for the `massechet=XXX` parameter

### Examples

```python
# Download single daf (both amudim) - שבועות
download_daf_range(308, 'מ', 'א', 'מ', 'ב')

# Download range of dafim - שבועות
download_daf_range(308, 'לח', 'א', 'מב', 'ב')

# Download only amud א for multiple dafim - שבועות
download_daf_range(308, 'מ', 'א', 'מג', 'א')

# Download different tractate (e.g., ברכות)
download_daf_range(283, 'ב', 'א', 'ה', 'ב')

# Download שבת
download_daf_range(284, 'ב', 'א', 'י', 'ב')

# Download higher range (for larger massechtot)
# Example: Download from דף קנ to דף קעו
download_daf_range(286, 'קנ', 'א', 'קעו', 'ב')
```

## Output

- Files are saved in `downloaded_pages/` directory
- Each file is named with Hebrew title (e.g., "שבועות מ עא.html")
- Files include:
  - Hebrew title as h1 heading
  - פירוש שטיינזלץ content
  - Source URL for reference
  - RTL Hebrew formatting

## Supported Hebrew Numbers

The script supports Hebrew daf notation from ב (2) through קעו (176):
ב, ג, ד, ה, ו, ז, ח, ט, י, יא, יב, יג, יד, טו, טז, יז, יח, יט, כ, כא, כב, כג, כד, כה, כו, כז, כח, כט, ל, לא, לב, לג, לד, לה, לו, לז, לח, לט, מ, מא, מב, מג, מד, מה, מו, מז, מח, מט, נ, נא, נב, נג, נד, נה, נו, נז, נח, נט, ס, סא, סב, סג, סד, סה, סו, סז, סח, סט, ע, עא, עב, עג, עד, עה, עו, עז, עח, עט, פ, פא, פב, פג, פד, פה, פו, פז, פח, פט, צ, צא, צב, צג, צד, צה, צו, צז, צח, צט, ק, קא, קב, קג, קד, קה, קו, קז, קח, קט, קי, קיא, קיב, קיג, קיד, קטו, קטז, קיז, קיח, קיט, קכ, קכא, קכב, קכג, קכד, קכה, קכו, קכז, קכח, קכט, קל, קלא, קלב, קלג, קלד, קלה, קלו, קלז, קלח, קלט, קמ, קמא, קמב, קמג, קמד, קמה, קמו, קמז, קמח, קמט, קנ, קנא, קנב, קנג, קנד, קנה, קנו, קנז, קנח, קנט, קס, קסא, קסב, קסג, קסד, קסה, קסו, קסז, קסח, קסט, קע, קעא, קעב, קעג, קעד, קעה, קעו

## File Structure

Each downloaded HTML file contains:
- Proper Hebrew RTL formatting
- Hebrew title as h1 (e.g., שבועות מ ע"א) - appears only once
- פירוש שטיינזלץ content directly - no redundant headings
- Clean, minimal HTML structure
- No duplicate titles or unnecessary source URLs

## Run the Script

```bash
source venv/bin/activate
python download_daf_simple.py
```

The default example downloads שבועות דף מ-מג (8 files total). 