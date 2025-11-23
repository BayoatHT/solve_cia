import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_imports_partners(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse imports partners from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['imports_partners'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['imports_partners_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing imports_partners: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 26 >>> 'Imports - partners'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'imports_partners_note'
    # "text" - 'imports_partners'
    # --------------------------------------------------------------------------------------------------
    # ['imports_partners', 'imports_partners_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "China 18%, Canada 14%, Mexico 14%, Germany 5%, Japan 4% (2022)",
        "note": "<b>note:</b> top five import partners based on percentage share of imports"
    }
    parsed_data = parse_imports_partners(pass_data)
    print(parsed_data)
