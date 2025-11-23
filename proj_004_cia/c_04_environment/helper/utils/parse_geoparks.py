import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_geoparks(geoparks_data: dict, iso3Code: str = None) -> dict:
    """Parse geoparks data."""
    result = {
        "geoparks": {
            "total": None,
            "parks": [],
            "raw_text": None
        },
        "geoparks_note": ""
    }

    if not geoparks_data or not isinstance(geoparks_data, dict):
        return result

    # Parse total
    total_data = geoparks_data.get('total global geoparks and regional networks', {})
    if total_data and isinstance(total_data, dict):
        text = total_data.get('text', '')
        if text and text.upper() != 'NA':
            num_match = re.search(r'(\d+)', text)
            if num_match:
                result['geoparks']['total'] = int(num_match.group(1))

    # Parse individual geoparks
    parks_data = geoparks_data.get('global geoparks and regional networks', {})
    if parks_data and isinstance(parks_data, dict):
        text = parks_data.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            result['geoparks']['raw_text'] = cleaned
            # Split by semicolon
            parks = [p.strip() for p in cleaned.split(';') if p.strip()]
            result['geoparks']['parks'] = parks

    return result


if __name__ == "__main__":
    test_data = {
        "total global geoparks and regional networks": {"text": "5"},
        "global geoparks and regional networks": {"text": "Park A; Park B; Park C"}
    }
    print(parse_geoparks(test_data))
