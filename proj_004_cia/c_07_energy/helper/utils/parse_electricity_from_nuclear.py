import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_from_nuclear(pass_data: dict) -> dict:
    """Parse electricity from nuclear from CIA Energy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['electricity_from_nuclear'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing electricity_from_nuclear: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # Electricity - from nuclear fuels - text - 'electricity_nuclear_fuels'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_nuclear_fuels']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0% of total installed capacity (2017 est.)"
    }
    parsed_data = parse_electricity_from_nuclear(pass_data)
    print(parsed_data)
