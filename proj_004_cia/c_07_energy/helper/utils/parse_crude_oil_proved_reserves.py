import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_crude_oil_proved_reserves(pass_data: dict) -> dict:
    """Parse crude oil proved reserves from CIA Energy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['crude_oil_proved_reserves'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing crude_oil_proved_reserves: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'crude_oil_proved_reserves'
    # --------------------------------------------------------------------------------------------------
    # ['crude_oil_proved_reserves']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 bbl (1 January 2018 est.)"
    }
    parsed_data = parse_crude_oil_proved_reserves(pass_data)
    print(parsed_data)
