import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_from_fossil(pass_data: dict) -> dict:
    """Parse electricity from fossil from CIA Energy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['electricity_from_fossil'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing electricity_from_fossil: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'electricity_fossil_fuels'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_fossil_fuels']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "100% of total installed capacity (2016 est.)"
    }
    parsed_data = parse_electricity_from_fossil(pass_data)
    print(parsed_data)
