import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_energy_consumption_per_capita(pass_data: dict) -> dict:
    """Parse energy consumption per capita from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        # Data has nested structure like {"Total energy consumption per capita 2022": {"text": "..."}}
        for key, value in pass_data.items():
            if key == 'note':
                if isinstance(value, dict) and 'text' in value:
                    note = value['text']
                    if note and isinstance(note, str) and note.strip():
                        result['energy_per_capita_note'] = clean_text(note)
                continue
            if isinstance(value, dict) and 'text' in value:
                text = value['text']
                if text and isinstance(text, str):
                    parsed = parse_energy_value(text)
                    if parsed['value'] is not None:
                        result['energy_per_capita_value'] = parsed['value']
                    if parsed['unit']:
                        result['energy_per_capita_unit'] = parsed['unit']
                    if parsed['year']:
                        result['energy_per_capita_year'] = parsed['year']
                    if parsed['is_estimate']:
                        result['energy_per_capita_is_estimate'] = parsed['is_estimate']
                    break
    except Exception as e:
        logging.error(f"Error parsing energy_consumption_per_capita: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # GET MORE FROM WORLD BANK
    # "Total energy consumption per capita 2022" - 'energy_consumption_per_capita_2022'
    # "note" - 'energy_consumption_per_capita_note'
    # --------------------------------------------------------------------------------------------------
    # ['energy_consumption_per_capita_2022', 'energy_consumption_per_capita_note']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Total energy consumption per capita 2022": {
            "text": "284.575 million Btu/person (2022 est.)"
        }
    }
    parsed_data = parse_energy_consumption_per_capita(pass_data)
    print(parsed_data)
