"""
Parse civil aircraft registration country code prefix from CIA World Factbook.
"""
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_civil_reg_code(civil_data: dict, iso3Code: str = None) -> dict:
    """
    Parse civil aircraft registration country code prefix.

    Args:
        civil_data: Dict with 'text' containing the country code prefix
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - civil_aircraft_code: str (e.g., "N" for USA, "F" for France)

    Example:
        Input: {"text": "N"}
        Output: {'civil_aircraft_code': 'N'}
    """
    result = {}

    if not civil_data:
        return result

    try:
        if 'text' in civil_data:
            text = civil_data['text']
            if text and isinstance(text, str) and text.strip():
                result['civil_aircraft_code'] = clean_text(text.strip())

    except Exception as e:
        logging.error(f"Error parsing civil_reg_code for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {"text": "N"}
    parsed = parse_civil_reg_code(test_data, "USA")
    print(parsed)
