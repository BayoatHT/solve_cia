import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_lakes(lakes_data: dict, iso3Code: str = None) -> dict:
    """Parse major lakes data."""
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
        """Parse lakes from text like 'Michigan – 57,750 sq km; Superior* – 53,348 sq km'"""
        lakes = []
        if not text:
            return lakes

        # Pattern: Lake name – area sq km
        pattern = re.compile(r'([A-Za-z\s\*\'\.]+?)\s*[–-]\s*([\d,]+)\s*sq\s*km', re.IGNORECASE)
        matches = pattern.findall(text)

        for name, area in matches:
            name = name.strip().rstrip('*')
            if name:
                lakes.append({
                    'name': name,
                    'area_sq_km': int(area.replace(',', ''))
                })
        return lakes

    # Parse fresh water lakes
    fresh = lakes_data.get('fresh water lake(s)', {})
    if fresh and isinstance(fresh, dict):
        text = fresh.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            result['major_lakes']['fresh_water'] = parse_lake_list(cleaned)
            if not result['major_lakes']['raw_text']:
                result['major_lakes']['raw_text'] = cleaned

    # Parse salt water lakes
    salt = lakes_data.get('salt water lake(s)', {})
    if salt and isinstance(salt, dict):
        text = salt.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            result['major_lakes']['salt_water'] = parse_lake_list(cleaned)

    return result


if __name__ == "__main__":
    test_data = {
        "fresh water lake(s)": {"text": "Michigan – 57,750 sq km; Superior* – 53,348 sq km"},
        "salt water lake(s)": {"text": "Great Salt – 4,360 sq km"}
    }
    print(parse_major_lakes(test_data))
