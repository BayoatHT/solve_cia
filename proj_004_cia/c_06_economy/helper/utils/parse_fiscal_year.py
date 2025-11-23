import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_fiscal_year(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse fiscal year from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['fiscal_year'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['fiscal_year_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing fiscal_year: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 15 >>> 'Fiscal year'
    # --------------------------------------------------------------------------------------------------
    # text - 'fiscal_year'
    # --------------------------------------------------------------------------------------------------
    # ['fiscal_year']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "calendar year"
    }
    parsed_data = parse_fiscal_year(pass_data)
    print(parsed_data)
