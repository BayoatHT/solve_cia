"""
Parse waterways data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_waterways(waterways_data: dict, iso3Code: str = None) -> dict:
    """
    Parse waterways data into structured format.

    Args:
        waterways_data: Dict with 'text' and optional 'note' keys
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - waterways_total_value: float (km of waterways)
            - waterways_total_unit: str ('km')
            - waterways_total_year: int (data year)
            - waterways_description: str (additional info from text)
            - waterways_note: str (optional note)

    Example:
        Input: {"text": "41,009 km (2012) (19,312 km used for commerce)"}
        Output: {
            'waterways_total_value': 41009.0,
            'waterways_total_unit': 'km',
            'waterways_total_year': 2012,
            'waterways_description': '19,312 km used for commerce'
        }
    """
    result = {}

    if not waterways_data:
        return result

    try:
        if 'text' in waterways_data:
            text = waterways_data['text']
            parsed = parse_transport_value(text)

            if parsed['value'] is not None:
                result['waterways_total_value'] = parsed['value']
            if parsed['unit']:
                result['waterways_total_unit'] = parsed['unit']
            if parsed['year']:
                result['waterways_total_year'] = parsed['year']

            # Extract additional description from parenthetical notes
            # Pattern: main value (year) (description)
            desc_match = re.search(r'\(\d{4}\)\s*\(([^)]+)\)', text)
            if desc_match:
                result['waterways_description'] = clean_text(desc_match.group(1))

        if 'note' in waterways_data:
            note = waterways_data['note']
            if note and isinstance(note, str) and note.strip():
                result['waterways_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing waterways for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "text": "41,009 km (2012) (19,312 km used for commerce; Saint Lawrence Seaway of 3,769 km)",
        "note": ""
    }
    parsed = parse_waterways(test_data, "USA")
    print(parsed)
