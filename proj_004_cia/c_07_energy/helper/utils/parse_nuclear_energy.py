import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_nuclear_energy(pass_data: dict) -> dict:
    """Parse nuclear energy from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        field_mappings = {
            'Number of operational nuclear reactors': 'nuclear_reactors',
            'Net capacity of operational nuclear reactors': 'nuclear_capacity',
            'Percent of total electricity production': 'nuclear_pct',
            'Number of nuclear reactors permanently shut down': 'nuclear_shutdown',
            'Number of nuclear reactors under construction': 'nuclear_construction'
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
    except Exception as e:
        logging.error(f"Error parsing nuclear_energy: {e}")
    return result
    try:
        field_mappings = {
            'Number of operational nuclear reactors': 'nuclear_operational_reactors',
            'Net capacity of operational nuclear reactors': 'nuclear_operational_reactors_capacity',
            'Percent of total electricity production': 'nuclear_percent_total_electricity',
            'Number of nuclear reactors permanently shut down': 'nuclear_reactors_shut_down',
            'Number of nuclear reactors under construction': 'nuclear_reactors_under_construction',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in pass_data:
                field_data = pass_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing nuclear_energy: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Net capacity of operational nuclear reactors" - 'nuclear_operational_reactors_capacity'
    # "Number of nuclear reactors permanently shut down" - 'nuclear_reactors_shut_down'
    # "Number of nuclear reactors under construction" - 'nuclear_reactors_under_construction'
    # "Number of operational nuclear reactors" - 'nuclear_operational_reactors'
    # "Percent of total electricity production" - 'nuclear_percent_total_electricity'
    # --------------------------------------------------------------------------------------------------
    # ['nuclear_operational_reactors_capacity', 'nuclear_reactors_shut_down', 'nuclear_reactors_under_construction',
    # 'nuclear_operational_reactors', 'nuclear_percent_total_electricity']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Number of operational nuclear reactors": {
            "text": "94 (2023)"
        },
        "Net capacity of operational nuclear reactors": {
            "text": "96.95GW (2023 est.)"
        },
        "Percent of total electricity production": {
            "text": "18.5% (2023 est.)"
        },
        "Number of nuclear reactors permanently shut down": {
            "text": "41 (2023)"
        }
    }
    parsed_data = parse_nuclear_energy(pass_data)
    print(parsed_data)
