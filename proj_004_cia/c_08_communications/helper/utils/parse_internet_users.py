import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_08_communications.helper.utils.parse_comms_value import parse_comms_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_internet_users(internet_users_data: dict) -> dict:
    """Parse internet users from CIA Communications section with separated value components."""
    result = {}
    if not internet_users_data or not isinstance(internet_users_data, dict):
        return result
    try:
        field_mappings = {
            'total': 'internet_users_total',
            'percent of population': 'internet_users_pct'
        }
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in internet_users_data:
                field_data = internet_users_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        parsed = parse_comms_value(text)
                        if parsed['value'] is not None:
                            result[f'{output_prefix}_value'] = parsed['value']
                        if parsed['unit']:
                            result[f'{output_prefix}_unit'] = parsed['unit']
                        if parsed['year']:
                            result[f'{output_prefix}_year'] = parsed['year']
                        if parsed['is_estimate']:
                            result[f'{output_prefix}_is_estimate'] = parsed['is_estimate']
        if 'note' in internet_users_data:
            note_data = internet_users_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['internet_users_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['internet_users_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing internet_users: {e}")
    return result
    try:
        field_mappings = {
            'total': 'internet_users_total',
            'percent of population': 'internet_users_percent',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in internet_users_data:
                field_data = internet_users_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in internet_users_data:
            note_data = internet_users_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['internet_users_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['internet_users_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing internet_users: {e}")
    return result


# Example usage
if __name__ == "__main__":
    internet_users_data = {
        "total": {
            "text": "312.8 million (2021 est.)"
        },
        "percent of population": {
            "text": "92% (2021 est.)"
        }
    }
    parsed_data = parse_internet_users(internet_users_data)
    print(parsed_data)
