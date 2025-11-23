import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_rivers(rivers_data: dict, iso3Code: str = None) -> dict:
    """Parse major rivers data."""
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

        # Try to parse rivers: "Missouri - 3,768 km; Mississippi - 3,544 km"
        # Pattern: River name - length km
        river_pattern = re.compile(r'([A-Za-z\s\-\'\.]+?)\s*[-–]\s*([\d,]+)\s*km')
        matches = river_pattern.findall(cleaned)

        for name, length in matches:
            name = name.strip().rstrip(' -')
            # Clean name from annotations like (shared with...)
            name = re.sub(r'\([^)]*\)', '', name).strip()
            if name:
                result['major_rivers']['rivers'].append({
                    'name': name,
                    'length_km': int(length.replace(',', ''))
                })

    return result


if __name__ == "__main__":
    test_data = {"text": "Missouri - 3,768 km; Mississippi - 3,544 km"}
    print(parse_major_rivers(test_data))
