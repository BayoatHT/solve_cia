import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_aquifers(aquifer_data: dict, iso3Code: str = None) -> dict:
    """Parse major aquifers data."""
    result = {
        "major_aquifers": {
            "aquifers": [],
            "raw_text": None
        },
        "major_aquifers_note": ""
    }

    if not aquifer_data or not isinstance(aquifer_data, dict):
        return result

    text = aquifer_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['major_aquifers']['raw_text'] = cleaned

        # Split by comma or semicolon
        parts = re.split(r'[,;]', cleaned)
        for part in parts:
            part = part.strip()
            if part and len(part) > 2:
                result['major_aquifers']['aquifers'].append(part)

    return result


if __name__ == "__main__":
    test_data = {"text": "Northern Great Plains Aquifer, Californian Central Valley Aquifer System"}
    print(parse_major_aquifers(test_data))
