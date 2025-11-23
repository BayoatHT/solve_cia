"""
Parse heliports data from CIA World Factbook Transportation section.
"""
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_heliports(heliports_data: dict, iso3Code: str = None) -> dict:
    """
    Parse heliports data into structured format.

    Args:
        heliports_data: Dict with 'text' and optional 'note' keys
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - heliports_total_value: int (number of heliports)
            - heliports_total_year: int (data year)
            - heliports_total_is_estimate: bool
            - heliports_note: str (optional note)

    Example:
        Input: {"text": "7,914 (2024)"}
        Output: {'heliports_total_value': 7914, 'heliports_total_year': 2024}
    """
    result = {}

    if not heliports_data:
        return result

    try:
        # Parse the main text field
        if 'text' in heliports_data:
            text = heliports_data['text']
            parsed = parse_transport_value(text)

            if parsed['value'] is not None:
                result['heliports_total_value'] = int(parsed['value'])
            if parsed['year']:
                result['heliports_total_year'] = parsed['year']
            if parsed['is_estimate']:
                result['heliports_total_is_estimate'] = parsed['is_estimate']

        # Parse note if present
        if 'note' in heliports_data:
            note = heliports_data['note']
            if note and isinstance(note, str) and note.strip():
                result['heliports_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing heliports for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {"text": "7,914 (2024)"}
    parsed = parse_heliports(test_data, "USA")
    print(parsed)
