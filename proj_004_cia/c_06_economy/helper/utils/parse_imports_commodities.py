import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_imports_commodities(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse imports commodities from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['imports_commodities'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['imports_commodities_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing imports_commodities: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 25 >>> 'Imports - commodities'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'imports_commodities_note'
    # "text" - 'imports_commodities'
    # --------------------------------------------------------------------------------------------------
    # ['imports_commodities', 'imports_commodities_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "crude petroleum, cars, broadcasting equipment, garments, computers (2022)",
        "note": "<b>note:</b> top five import commodities based on value in dollars"
    }
    parsed_data = parse_imports_commodities(pass_data)
    print(parsed_data)
