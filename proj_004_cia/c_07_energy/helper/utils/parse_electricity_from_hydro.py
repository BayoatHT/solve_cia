import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_from_hydro(pass_data: dict) -> dict:
    """Parse electricity from hydro from CIA Energy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['elec_hydro_value'] = parsed['value']
                if parsed['unit']:
                    result['elec_hydro_unit'] = parsed['unit']
                if parsed['year']:
                    result['elec_hydro_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['elec_hydro_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logging.error(f"Error parsing electricity_from_hydro: {e}")
    return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['electricity_from_hydro'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing electricity_from_hydro: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'electricity_hydroelectric'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_hydroelectric']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0% of total installed capacity (2017 est.)"
    }
    parsed_data = parse_electricity_from_hydro(pass_data)
    print(parsed_data)
