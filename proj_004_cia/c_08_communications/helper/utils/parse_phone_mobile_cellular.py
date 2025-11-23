import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_08_communications.helper.utils.parse_comms_value import parse_comms_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_phone_mobile_cellular(mobile_cellular_data: dict) -> dict:
    """Parse phone mobile cellular from CIA Communications section with separated value components."""
    result = {}
    if not mobile_cellular_data or not isinstance(mobile_cellular_data, dict):
        return result
    try:
        field_mappings = {
            'total subscriptions': 'mobile_phone_total',
            'subscriptions per 100 inhabitants': 'mobile_phone_per_100'
        }
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in mobile_cellular_data:
                field_data = mobile_cellular_data[cia_key]
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
        if 'note' in mobile_cellular_data:
            note_data = mobile_cellular_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['mobile_phone_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['mobile_phone_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing phone_mobile_cellular: {e}")
    return result
    try:
        field_mappings = {
            'total subscriptions': 'mobile_phone_total_subs',
            'subscriptions per 100 inhabitants': 'mobile_phone_subs_per_100',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in mobile_cellular_data:
                field_data = mobile_cellular_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in mobile_cellular_data:
            note_data = mobile_cellular_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['mobile_phone_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['mobile_phone_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing phone_mobile_cellular: {e}")
    return result


# Example usage
if __name__ == "__main__":
    mobile_cellular_data = {
        "total subscriptions": {
            "text": "372.682 million (2022 est.)"
        },
        "subscriptions per 100 inhabitants": {
            "text": "110 (2022 est.)"
        }
    }
    parsed_data = parse_phone_mobile_cellular(mobile_cellular_data)
    print(parsed_data)
