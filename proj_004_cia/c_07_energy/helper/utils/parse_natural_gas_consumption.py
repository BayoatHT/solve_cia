import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_natural_gas_consumption(pass_data: dict) -> dict:
    """Parse natural gas consumption from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['nat_gas_consumption_value'] = parsed['value']
                if parsed['unit']:
                    result['nat_gas_consumption_unit'] = parsed['unit']
                if parsed['year']:
                    result['nat_gas_consumption_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['nat_gas_consumption_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logging.error(f"Error parsing natural_gas_consumption: {e}")
    return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['natural_gas_consumption'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing natural_gas_consumption: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'natural_gas_consumption'
    # --------------------------------------------------------------------------------------------------
    # ['natural_gas_consumption']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 cu m (2017 est.)"
    }
    parsed_data = parse_natural_gas_consumption(pass_data)
    print(parsed_data)
