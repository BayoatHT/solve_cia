import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_broadband_fixed(broadband_fixed_data: dict) -> dict:
    """Parse broadband fixed subscriptions from CIA Communications section."""
    result = {}
    if not broadband_fixed_data or not isinstance(broadband_fixed_data, dict):
        return result
    try:
        field_mappings = {
            'total': 'broadband_total',
            'subscriptions per 100 inhabitants': 'broadband_subs_per_100',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in broadband_fixed_data:
                field_data = broadband_fixed_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in broadband_fixed_data:
            note_data = broadband_fixed_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['broadband_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['broadband_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing broadband_fixed: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # "note" - 'broadband_note'
    # "subscriptions per 100 inhabitants" - 'broadband_subs_per_100'
    # "total" - 'broadband_total'
    # --------------------------------------------------------------------------------------------------
    # ['broadband_note', 'broadband_subs_per_100', 'broadband_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    broadband_fixed_data = {
        "total": {
            "text": "121.176 million (2020 est.)"
        },
        "subscriptions per 100 inhabitants": {
            "text": "37 (2020 est.)"
        }
    }
    parsed_data = parse_broadband_fixed(broadband_fixed_data)
    print(parsed_data)
