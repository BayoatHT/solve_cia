import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_lakes(lakes_data: dict, iso3Code: str = None) -> dict:
    """
    Parse major lakes data from CIA World Factbook.

    Handles formats like:
    - "Michigan – 57,750 sq km; Superior* – 53,348 sq km"
    - "Lake Chad (endorheic lake shared with Niger, Chad, and Cameroon) - 10,360-25,900 sq km"
    - "Lake Tanganyika (shared with Burundi, Tanzania, and Zambia) - 32,000 sq km"
    """
    result = {
        "major_lakes": {
            "fresh_water": [],
            "salt_water": [],
            "raw_text": None
        },
        "major_lakes_note": ""
    }

    if not lakes_data or not isinstance(lakes_data, dict):
        return result

    def parse_lake_list(text):
        """Parse lakes from various text formats."""
        lakes = []
        if not text:
            return lakes

        # Extract note if present
        note = ""
        note_match = re.search(r'note\s*[-–:]\s*(.+?)(?:$)', text, re.IGNORECASE)
        if note_match:
            note = note_match.group(1).strip()

        # Split by semicolons, handling entries that may contain notes
        entries = re.split(r';\s*', text)

        for entry in entries:
            # Skip notes and empty entries
            if not entry or entry.lower().startswith('note'):
                continue

            # Skip entries with non-numeric values like "largely dried up"
            if not re.search(r'\d', entry):
                continue

            # Pattern 1: Standard format with dash - "Name - NUMBER sq km" or "Name - MIN-MAX sq km"
            match = re.search(r'^(.+?)\s*[-–]\s*([\d,]+(?:\s*[-–]\s*[\d,]+)?)\s*sq\s*km', entry.strip(), re.IGNORECASE)

            # Pattern 2: Missing "sq km" - "Name - NUMBER"
            if not match:
                match = re.search(r'^(.+?)\s*[-–]\s*([\d,]+)\s*$', entry.strip())

            # Pattern 3: No dash - "Name NUMBER sq km" (like "Biwa-ko 688 sq km")
            if not match:
                match = re.search(r'^(.+?)\s+([\d,]+)\s*sq\s*km', entry.strip(), re.IGNORECASE)
            if match:
                raw_name = match.group(1).strip()
                area_str = match.group(2)

                # Parse area - handle ranges like "10,360-25,900"
                area_parts = re.findall(r'[\d,]+', area_str)
                if len(area_parts) >= 2:
                    area_min = int(area_parts[0].replace(',', ''))
                    area_max = int(area_parts[1].replace(',', ''))
                    area = None  # Use range instead
                elif area_parts:
                    area = int(area_parts[0].replace(',', ''))
                    area_min = None
                    area_max = None
                else:
                    continue

                # Extract shared info - handle both "shared with X" and "endorheic lake shared with X"
                shared_with = []
                shared_match = re.search(r'shared with\s+([^)]+)', raw_name, re.IGNORECASE)
                if shared_match:
                    shared_text = shared_match.group(1)
                    # Parse countries - handle "X and Y", "X, Y, and Z", "X, Y"
                    # Replace " and " with comma for uniform splitting
                    shared_text = re.sub(r'\s+and\s+', ', ', shared_text)
                    countries = [c.strip() for c in shared_text.split(',') if c.strip()]
                    shared_with = countries

                # Check for ephemeral flag
                is_ephemeral = 'ephemeral' in raw_name.lower()

                # Clean name - remove annotations but keep "Lake" prefix if present
                name = re.sub(r'\s*\([^)]*\)\s*', ' ', raw_name).strip()
                name = name.rstrip('*').strip()

                if name:
                    lake_data = {'name': name}

                    if area is not None:
                        lake_data['area_sq_km'] = area
                    else:
                        lake_data['area_sq_km_min'] = area_min
                        lake_data['area_sq_km_max'] = area_max

                    if shared_with:
                        lake_data['shared_with'] = shared_with
                    if is_ephemeral:
                        lake_data['is_ephemeral'] = True

                    lakes.append(lake_data)

        return lakes, note

    # Parse fresh water lakes
    fresh = lakes_data.get('fresh water lake(s)', {})
    if fresh and isinstance(fresh, dict):
        text = fresh.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            lakes, note = parse_lake_list(cleaned)
            result['major_lakes']['fresh_water'] = lakes
            if note:
                result['major_lakes_note'] = note
            if not result['major_lakes']['raw_text']:
                result['major_lakes']['raw_text'] = cleaned

    # Parse salt water lakes
    salt = lakes_data.get('salt water lake(s)', {})
    if salt and isinstance(salt, dict):
        text = salt.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            lakes, note = parse_lake_list(cleaned)
            result['major_lakes']['salt_water'] = lakes
            if note and not result['major_lakes_note']:
                result['major_lakes_note'] = note
            # Append to raw_text if fresh water already set it
            if result['major_lakes']['raw_text']:
                result['major_lakes']['raw_text'] += "; " + cleaned
            else:
                result['major_lakes']['raw_text'] = cleaned

    return result


if __name__ == "__main__":
    # Test various formats
    test_cases = [
        {
            "fresh water lake(s)": {"text": "Michigan – 57,750 sq km; Superior* – 53,348 sq km"},
            "salt water lake(s)": {"text": "Great Salt – 4,360 sq km"}
        },
        {
            "fresh water lake(s)": {"text": "Lake Chad (endorheic lake shared with Niger, Chad, and Cameroon) - 10,360-25,900 sq km<br>note - area varies by season and year to year"}
        },
        {
            "salt water lake(s)": {"text": "Lake Eyre - 9,690 sq km; Lake Torrens (ephemeral) - 5,780 sq km"}
        }
    ]
    from pprint import pprint
    for test in test_cases:
        print("Input:", test)
        result = parse_major_lakes(test)
        pprint(result)
        print()
