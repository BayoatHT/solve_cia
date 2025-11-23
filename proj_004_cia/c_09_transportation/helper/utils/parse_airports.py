"""
Parse airports data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_airports(airports_data: dict, iso3Code: str = None) -> dict:
    """
    Parse airports data into structured format.

    Args:
        airports_data: Dict with 'text' and optional 'note' keys
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - airports_total_value: int (number of airports)
            - airports_total_year: int (data year)
            - airports_total_is_estimate: bool
            - airports_note: str (optional note)

    Example:
        Input: {"text": "15,873 (2024)"}
        Output: {'airports_total_value': 15873, 'airports_total_year': 2024}
    """
    result = {}

    if not airports_data:
        return result

    try:
        # Parse the main text field
        if 'text' in airports_data:
            text = airports_data['text']
            parsed = parse_transport_value(text)

            if parsed['value'] is not None:
                result['airports_total_value'] = int(parsed['value'])
            if parsed['year']:
                result['airports_total_year'] = parsed['year']
            if parsed['is_estimate']:
                result['airports_total_is_estimate'] = parsed['is_estimate']

        # Parse note if present
        if 'note' in airports_data:
            note = airports_data['note']
            if note and isinstance(note, str) and note.strip():
                result['airports_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing airports for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "text": "15,873 (2024)",
        "note": ""
    }
    parsed = parse_airports(test_data, "USA")
    print(parsed)
