import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_crude_oil_production(pass_data: dict) -> dict:
    """Parse crude oil production from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['crude_production_value'] = parsed['value']
                if parsed['unit']:
                    result['crude_production_unit'] = parsed['unit']
                if parsed['year']:
                    result['crude_production_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['crude_production_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logging.error(f"Error parsing crude_oil_production: {e}")
    return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['crude_oil_production'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing crude_oil_production: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'crude_oil_production'
    # --------------------------------------------------------------------------------------------------
    # ['crude_oil_production']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 bbl/day (2018 est.)"
    }
    parsed_data = parse_crude_oil_production(pass_data)
    print(parsed_data)
