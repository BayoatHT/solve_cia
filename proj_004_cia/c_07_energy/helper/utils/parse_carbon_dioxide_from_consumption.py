import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_carbon_dioxide_from_consumption(carbon_data: dict) -> dict:
    """Parse carbon dioxide from consumption from CIA Energy section with separated value components."""
    result = {}
    if not carbon_data or not isinstance(carbon_data, dict):
        return result
    try:
        if 'text' in carbon_data:
            text = carbon_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['co2_energy_value'] = parsed['value']
                if parsed['unit']:
                    result['co2_energy_unit'] = parsed['unit']
                if parsed['year']:
                    result['co2_energy_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['co2_energy_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logging.error(f"Error parsing carbon_dioxide_from_consumption: {e}")
    return result
    try:
        if 'text' in carbon_data:
            text = carbon_data['text']
            if text and isinstance(text, str):
                result['co2_emissions_energy_consumption'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing carbon_dioxide_from_consumption: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'co2_emissions_energy_consumption'
    # --------------------------------------------------------------------------------------------------
    # ['co2_emissions_energy_consumption']
    # --------------------------------------------------------------------------------------------------
    carbon_data = {
        "text": "268,400 Mt (2017 est.)"
    }
    parsed_data = parse_carbon_dioxide_from_consumption(carbon_data)
    print(parsed_data)
