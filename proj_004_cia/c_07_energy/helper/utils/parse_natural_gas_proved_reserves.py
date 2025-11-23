import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_natural_gas_proved_reserves(pass_data: dict) -> dict:
    """Parse natural gas proved reserves from CIA Energy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['natural_gas_proved_reserves'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing natural_gas_proved_reserves: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'natural_gas_proved_reserves'
    # --------------------------------------------------------------------------------------------------
    # ['natural_gas_proved_reserves']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 cu m (1 January 2014 est.)"
    }
    parsed_data = parse_natural_gas_proved_reserves(pass_data)
    print(parsed_data)
