import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_internet_code(internet_code_data: dict) -> dict:
    """Parse internet country code from CIA Communications section."""
    result = {}
    if not internet_code_data or not isinstance(internet_code_data, dict):
        return result
    try:
        if 'text' in internet_code_data:
            text = internet_code_data['text']
            if text and isinstance(text, str):
                result['internet_country_code'] = clean_text(text)
        if 'note' in internet_code_data:
            note_data = internet_code_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['internet_country_code_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['internet_country_code_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing internet_code: {e}")
    return result


# Example usage
if __name__ == "__main__":
    internet_code_data = {
        "text": ".us"
    }
    parsed_data = parse_internet_code(internet_code_data)
    print(parsed_data)
