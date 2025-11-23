import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_carbon_dioxide_from_consumption(carbon_data: dict) -> dict:
    """Parse CO2 emissions from energy consumption from CIA Energy section."""
    result = {}
    if not carbon_data or not isinstance(carbon_data, dict):
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
