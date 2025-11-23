import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_watersheds(watershed_data: dict, iso3Code: str = None) -> dict:
    """Parse major watersheds data."""
    result = {
        "major_watersheds": {
            "watersheds": [],
            "raw_text": None
        },
        "major_watersheds_note": ""
    }

    if not watershed_data or not isinstance(watershed_data, dict):
        return result

    text = watershed_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['major_watersheds']['raw_text'] = cleaned

        # Parse pattern: "Name (area sq km)" or "Name* (area sq km)"
        pattern = re.compile(r'([A-Za-z\s\*\']+?)\s*\(([\d,]+)\s*sq\s*km', re.IGNORECASE)
        matches = pattern.findall(cleaned)

        for name, area in matches:
            name = name.strip().rstrip('*')
            if name:
                result['major_watersheds']['watersheds'].append({
                    'name': name,
                    'area_sq_km': int(area.replace(',', ''))
                })

    return result


if __name__ == "__main__":
    test_data = {"text": "Mississippi* (3,202,185 sq km); Rio Grande (607,965 sq km)"}
    print(parse_major_watersheds(test_data))
