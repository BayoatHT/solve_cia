import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_rivers(rivers_data: dict, iso3Code: str = None) -> dict:
    """
    Parse major rivers data from CIA World Factbook.

    Handles formats like:
    - "Missouri - 3,768 km; Mississippi - 3,544 km"
    - "Yukon river mouth (shared with Canada [s]) - 3,190 km"
    - "Niger river mouth (shared with Guinea [s], Mali, Benin, and Niger) - 4,200 km"
    """
    result = {
        "major_rivers": {
            "rivers": [],
            "raw_text": None
        },
        "major_rivers_note": ""
    }

    if not rivers_data or not isinstance(rivers_data, dict):
        return result

    text = rivers_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['major_rivers']['raw_text'] = cleaned

        # Split off notes to avoid "1,006note" issues from HTML br tags
        # Add space before "note" if it's directly after a number
        cleaned = re.sub(r'(\d)note\b', r'\1 note', cleaned, flags=re.IGNORECASE)

        # Extract note if present
        note_match = re.search(r'note\s*[-–:]\s*(.+?)(?:$|;(?!\s*\d))', cleaned, re.IGNORECASE)
        if note_match:
            result['major_rivers_note'] = note_match.group(1).strip()

        # Split by semicolons first, then parse each river entry
        # Handle entries like "Missouri - 3,768 km" or "Yukon river mouth (shared with Canada [s]) - 3,190 km"
        entries = re.split(r';\s*', cleaned)

        for entry in entries:
            # Skip notes, empty entries, and headers
            if not entry or entry.lower().startswith('note') or entry.endswith(':'):
                continue
            # Skip list headers like "top ten longest rivers:"
            if ':' in entry and not re.search(r'\d', entry.split(':')[0]):
                entry = entry.split(':', 1)[1].strip()
                if not entry:
                    continue

            # Strip trailing note text that might have been merged from HTML
            entry = re.sub(r'\s*note\s*[-–:].*$', '', entry.strip(), flags=re.IGNORECASE)

            # Pattern 1: Standard format "Name - NUMBER km"
            match = re.search(r'^(.+?)\s*[-–]\s*([\d,]+)\s*km', entry.strip())

            # Pattern 2: Missing "km" - "Name - NUMBER" (for entries like "- 1,006")
            if not match:
                match = re.search(r'^(.+?)\s*[-–]\s*([\d,]+)\s*$', entry.strip())

            # Pattern 3: World format without dash - "Name (Region) NUMBER km"
            if not match:
                match = re.search(r'^(.+?)\s+([\d,]+)\s*km', entry.strip())
            if match:
                raw_name = match.group(1).strip()
                length_str = match.group(2).replace(',', '')

                # Extract clean name and shared info
                shared_with = []
                shared_match = re.search(r'\(shared with\s+([^)]+)\)', raw_name, re.IGNORECASE)
                if shared_match:
                    shared_text = shared_match.group(1)
                    # Parse countries from "Guinea [s], Mali, Benin, and Niger"
                    countries = re.findall(r'([A-Za-z\s]+?)(?:\s*\[[sm]\])?(?:,\s*and\s*|,\s*|$)', shared_text)
                    shared_with = [c.strip() for c in countries if c.strip()]

                # Clean name - remove parenthetical annotations for the name field
                name = re.sub(r'\s*\([^)]*\)\s*', ' ', raw_name).strip()
                # Also clean "river mouth", "river source" prefixes for cleaner name
                display_name = name

                # Determine if this is source or mouth based on the river name portion
                # Check for [s] or [m] BEFORE the dash (in the name), not in shared_with text
                name_part = raw_name.lower()
                is_source = 'source' in name_part or 'river source' in name_part
                is_mouth = 'mouth' in name_part or 'river mouth' in name_part

                if name:
                    river_data = {
                        'name': display_name,
                        'length_km': int(length_str)
                    }
                    if shared_with:
                        river_data['shared_with'] = shared_with
                    if is_source:
                        river_data['is_source'] = True
                    if is_mouth:
                        river_data['is_mouth'] = True

                    result['major_rivers']['rivers'].append(river_data)

    return result


if __name__ == "__main__":
    # Test various formats
    test_cases = [
        {"text": "Missouri - 3,768 km; Mississippi - 3,544 km"},
        {"text": "<p>Missouri - 3,768 km; Yukon river mouth (shared with Canada [s]) - 3,190 km</p>"},
        {"text": "Niger river mouth (shared with Guinea [s], Mali, Benin, and Niger) - 4,200 km"},
    ]
    for test in test_cases:
        print(f"Input: {test['text'][:60]}...")
        result = parse_major_rivers(test)
        print(f"Rivers: {result['major_rivers']['rivers']}")
        print()
