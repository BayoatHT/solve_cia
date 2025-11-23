import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity(pass_data: dict) -> dict:
    """Parse electricity from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        field_mappings = {
            'installed generating capacity': 'elec_capacity',
            'consumption': 'elec_consumption',
            'exports': 'elec_exports',
            'imports': 'elec_imports',
            'transmission/distribution losses': 'elec_losses'
        }
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in pass_data:
                field_data = pass_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        parsed = parse_energy_value(text)
                        if parsed['value'] is not None:
                            result[f'{output_prefix}_value'] = parsed['value']
                        if parsed['unit']:
                            result[f'{output_prefix}_unit'] = parsed['unit']
                        if parsed['year']:
                            result[f'{output_prefix}_year'] = parsed['year']
                        if parsed['is_estimate']:
                            result[f'{output_prefix}_is_estimate'] = parsed['is_estimate']
        if 'note' in pass_data:
            note_data = pass_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['electricity_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['electricity_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing electricity: {e}")
    return result
    try:
        field_mappings = {
            'installed generating capacity': 'electricity_generating_capacity',
            'consumption': 'electricity_consumption',
            'exports': 'electricity_exports',
            'imports': 'electricity_imports',
            'transmission/distribution losses': 'electricity_transmission_distribution_losses',
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
                    result['electricity_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['electricity_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing electricity: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "consumption" - 'electricity_consumption'
    # "exports" - 'electricity_exports'
    # "imports" - 'electricity_imports'
    # "installed generating capacity" - 'electricity_generating_capacity'
    # "note" - 'electricity_note'
    # "transmission/distribution losses" - 'electricity_transmission_distribution_losses'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_consumption', 'electricity_exports', 'electricity_imports',
    # 'electricity_generating_capacity', 'electricity_note', 'electricity_transmission_distribution_losses']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "installed generating capacity": {
            "text": "1.201 billion kW (2022 est.)"
        },
        "consumption": {
            "text": "4.128 trillion kWh (2022 est.)"
        },
        "exports": {
            "text": "15.758 billion kWh (2022 est.)"
        },
        "imports": {
            "text": "56.97 billion kWh (2022 est.)"
        },
        "transmission/distribution losses": {
            "text": "204.989 billion kWh (2022 est.)"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_electricity(pass_data)
    print(parsed_data)
