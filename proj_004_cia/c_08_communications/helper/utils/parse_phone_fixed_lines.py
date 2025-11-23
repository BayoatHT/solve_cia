import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_phone_fixed_lines(phone_fixed_lines_data: dict) -> dict:
    """Parse fixed line telephones from CIA Communications section."""
    result = {}
    if not phone_fixed_lines_data or not isinstance(phone_fixed_lines_data, dict):
        return result
    try:
        field_mappings = {
            'total subscriptions': 'fixed_phone_total_subs',
            'subscriptions per 100 inhabitants': 'fixed_phone_subs_per_100',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in phone_fixed_lines_data:
                field_data = phone_fixed_lines_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in phone_fixed_lines_data:
            note_data = phone_fixed_lines_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['fixed_phone_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['fixed_phone_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing phone_fixed_lines: {e}")
    return result


# Example usage
if __name__ == "__main__":
    phone_fixed_lines_data = {
        "total subscriptions": {
            "text": "91.623 million (2022 est.)"
        },
        "subscriptions per 100 inhabitants": {
            "text": "27 (2022 est.)"
        },
        "note": ""
    }
    parsed_data = parse_phone_fixed_lines(phone_fixed_lines_data)
    print(parsed_data)
