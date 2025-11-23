import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_natural_gas(pass_data: dict) -> dict:
    """Parse natural gas from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        field_mappings = {
            'production': 'nat_gas_production',
            'consumption': 'nat_gas_consumption',
            'exports': 'nat_gas_exports',
            'imports': 'nat_gas_imports',
            'proven reserves': 'nat_gas_reserves'
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
                    result['natural_gas_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['natural_gas_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing natural_gas: {e}")
    return result
    try:
        field_mappings = {
            'production': 'natural_gas_production',
            'consumption': 'natural_gas_consumption',
            'exports': 'natural_gas_exports',
            'imports': 'natural_gas_imports',
            'proven reserves': 'natural_gas_proven_reserves',
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
                    result['natural_gas_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['natural_gas_note'] = clean_text(note_data)
    except Exception as e:
        logging.error(f"Error parsing natural_gas: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    # text - 'natural_gas'
    # --------------------------------------------------------------------------------------------------
    # ['natural_gas']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "production": {
            "text": "1.029 trillion cubic meters (2022 est.)"
        },
        "consumption": {
            "text": "914.301 billion cubic meters (2022 est.)"
        },
        "exports": {
            "text": "195.497 billion cubic meters (2022 est.)"
        },
        "imports": {
            "text": "85.635 billion cubic meters (2022 est.)"
        },
        "proven reserves": {
            "text": "13.402 trillion cubic meters (2021 est.)"
        }
    }
    parsed_data = parse_natural_gas(pass_data)
    print(parsed_data)
