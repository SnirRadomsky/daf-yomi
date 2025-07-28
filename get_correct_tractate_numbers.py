#!/usr/bin/env python3
"""
Script to get correct tractate numbers from daf-yomi.com
"""

# What we found so far
known_correct = {
    'ברכות': 283,
    'ביצה': 290,
    'יומא': 306,  # This one worked in our tests
}

# Updated TRACTATES dictionary with corrected numbers
# We'll systematically check a few more key ones
CORRECT_TRACTATES = {
    'ברכות': 283,
    'שבת': 302,     # Need to verify
    'עירובין': 303, # Need to verify  
    'פסחים': 304,   # Need to verify
    'שקלים': 305,   # Need to verify
    'יומא': 306,     # Confirmed working
    'סוכה': 307,     # Need to verify
    'ביצה': 290,     # Confirmed
    'ראש השנה': 312, # Need to verify
    'תענית': 313,    # Need to verify
    'מגילה': 314,   # Need to verify
    'מועד קטן': 315, # Need to verify
    'חגיגה': 316,   # Need to verify
    'יבמות': 317,   # Need to verify
    'כתובות': 318,  # Need to verify
    'נדרים': 319,   # Need to verify
    'נזיר': 320,     # Need to verify
    'סוטה': 321,     # Need to verify
    'גיטין': 322,    # Need to verify
    'קידושין': 323,  # Need to verify
    'בבא קמא': 324,  # Need to verify
    'בבא מציעא': 325, # Need to verify
    'בבא בתרא': 326, # Need to verify
    'סנהדרין': 327,  # Need to verify
    'מכות': 328,     # Need to verify
    'שבועות': 329,   # Need to verify
    'מנחות': 330,    # Need to verify
    'חולין': 331,     # Need to verify
    'בכורות': 332,    # Need to verify
    'ערכין': 333,     # Need to verify
    'תמורה': 334,     # Need to verify
    'כריתות': 335,    # Need to verify
    'מעילה': 336,     # Need to verify
    'תמיד': 337,      # Need to verify
    'מדות': 338,      # Need to verify
    'קינים': 339,     # Need to verify -> was קנים on site
    'נדה': 340,       # Need to verify -> was נידה on site
    'עבודה זרה': 309, # We have local files for this, need to verify number
    'הוריות': 310,    # We have local files for this, need to verify number  
    'זבחים': 311,     # We have local files for this, need to verify number
}

print("Corrected TRACTATES dictionary:")
for name, num in CORRECT_TRACTATES.items():
    print(f"    '{name}': {num},")