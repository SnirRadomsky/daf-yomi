#!/usr/bin/env python3
"""
Debug the file lookup logic
"""

import os

# Same Hebrew numbers mapping from the app
HEBREW_NUMBERS = {
    'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'יא': 11, 'יב': 12, 'יג': 13, 'יד': 14, 'טו': 15, 'טז': 16, 'יז': 17, 'יח': 18, 'יט': 19, 'כ': 20,
    'כא': 21, 'כב': 22, 'כג': 23, 'כד': 24, 'כה': 25, 'כו': 26, 'כז': 27, 'כח': 28, 'כט': 29, 'ל': 30,
    'לא': 31, 'לב': 32, 'לג': 33, 'לד': 34, 'לה': 35, 'לו': 36, 'לז': 37, 'לח': 38, 'לט': 39, 'מ': 40,
    'מא': 41, 'מב': 42, 'מג': 43, 'מד': 44, 'מה': 45, 'מו': 46, 'מז': 47, 'מח': 48, 'מט': 49, 'נ': 50,
    'נא': 51, 'נב': 52, 'נג': 53, 'נד': 54, 'נה': 55, 'נו': 56, 'נז': 57, 'נח': 58, 'נט': 59, 'ס': 60,
    'סא': 61, 'סב': 62, 'סג': 63, 'סד': 64, 'סה': 65, 'סו': 66, 'סז': 67, 'סח': 68, 'סט': 69, 'ע': 70,
    'עא': 71, 'עב': 72, 'עג': 73, 'עד': 74, 'עה': 75, 'עו': 76, 'עז': 77, 'עח': 78, 'עט': 79, 'פ': 80,
}

NUMBER_TO_HEBREW = {v: k for k, v in HEBREW_NUMBERS.items()}
TRACTATES = {'עבודה זרה': 309}

def debug_lookup():
    """Debug the file lookup"""
    # Test עבודה זרה סב עמוד א
    massechet_num = 309
    daf_hebrew = 'סב'
    amud = 'א'
    
    # Convert to amud number
    page_num = HEBREW_NUMBERS.get(daf_hebrew, 0)
    amud_num = (page_num - 1) * 2 + 1 if amud == 'א' else (page_num - 1) * 2 + 2
    
    print(f"Testing: עבודה זרה {daf_hebrew} {amud}")
    print(f"Page number: {page_num}")  
    print(f"Amud number: {amud_num}")
    
    # Now reverse it back
    massechet_names = {v: k for k, v in TRACTATES.items()}
    massechet_name = massechet_names.get(massechet_num, "")
    print(f"Massechet name: {massechet_name}")
    
    # Convert back
    daf_num = (amud_num + 1) // 2
    side = 'א' if amud_num % 2 == 1 else 'ב'
    daf_hebrew_back = NUMBER_TO_HEBREW.get(daf_num, str(daf_num))
    
    print(f"Converted back: amud_num={amud_num} -> daf_num={daf_num} -> {daf_hebrew_back} side={side}")
    print(f"amud_num % 2 = {amud_num % 2}")
    print(f"(amud_num + 1) // 2 = {(amud_num + 1) // 2}")
    
    # Look for the file
    pages_dir = "pages"
    possible_patterns = [
        f"{massechet_name} {daf_hebrew_back} ע{side}.html",
        f"{massechet_name} {daf_hebrew_back} ע\"{side}\".html", 
    ]
    
    for pattern in possible_patterns:
        file_path = os.path.join(pages_dir, pattern)
        print(f"Looking for: {file_path}")
        if os.path.exists(file_path):
            print(f"✅ FOUND: {file_path}")
            return
        else:
            print(f"❌ NOT FOUND: {file_path}")
    
    # List actual files
    print(f"\nActual files in {pages_dir}:")
    if os.path.exists(pages_dir):
        files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
        for f in sorted(files):
            if 'עבודה זרה' in f:
                print(f"  {f}")

if __name__ == "__main__":
    debug_lookup()