import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ease_of_business(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse ease of business from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['ease_of_business'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['ease_of_business_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing ease_of_business: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 9 >>> 'Ease of Doing Business Index scores'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {

    }
    parsed_data = parse_ease_of_business(pass_data)
    print(parsed_data)
