import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_petroleum(pass_data: dict) -> dict:
    """Parse petroleum data from CIA Energy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        field_mappings = {
            'total petroleum production': 'total_petroleum_production',
            'refined petroleum consumption': 'refined_petroleum_consumption',
            'crude oil estimated reserves': 'crude_oil_estimated_reserves',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in pass_data:
                field_data = pass_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in pass_data:
            note_data = pass_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['petroleum_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['petroleum_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing petroleum: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "crude oil estimated reserves" - 'crude_oil_estimated_reserves'
    # "note" - 'petroleum_note'
    # "refined petroleum consumption" - 'refined_petroleum_consumption'
    # "total petroleum production" - 'total_petroleum_production'
    # --------------------------------------------------------------------------------------------------
    # ['crude_oil_estimated_reserves', 'petroleum_note', 'refined_petroleum_consumption',
    # 'total_petroleum_production']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "total petroleum production": {
            "text": "20.879 million bbl/day (2023 est.)"
        },
        "refined petroleum consumption": {
            "text": "20.246 million bbl/day (2023 est.)"
        },
        "crude oil estimated reserves": {
            "text": "38.212 billion barrels (2021 est.)"
        }
    }
    parsed_data = parse_petroleum(pass_data)
    print(parsed_data)
