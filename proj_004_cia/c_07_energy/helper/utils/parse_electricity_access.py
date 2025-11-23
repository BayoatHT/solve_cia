import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_access(electricity_data: dict) -> dict:
    """Parse electricity access from CIA Energy section."""
    result = {}
    if not electricity_data or not isinstance(electricity_data, dict):
        return result
    try:
        field_mappings = {
            'electrification - total population': 'electricity_access_total_population',
            'electrification - urban areas': 'electricity_access_urban_areas',
            'electrification - rural areas': 'electricity_access_rural_areas',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in electricity_data:
                field_data = electricity_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
        if 'note' in electricity_data:
            note_data = electricity_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['electricity_access_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['electricity_access_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing electricity_access: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "electrification - rural areas" - 'electricity_access_rural_areas'
    # "electrification - total population" - 'electricity_access_total_population'
    # "electrification - urban areas" - 'electricity_access_urban_areas'
    # "note" - 'electricity_access_note'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_access_rural_areas', 'electricity_access_total_population',
    # 'electricity_access_urban_areas', 'electricity_access_note']
    electricity_data = {
        "electrification - total population": {
            "text": "100% (2022 est.)"
        },
        "electrification - urban areas": {
            "text": "100%"
        },
        "electrification - rural areas": {
            "text": "99.3%"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_electricity_access(electricity_data)
    print(parsed_data)
