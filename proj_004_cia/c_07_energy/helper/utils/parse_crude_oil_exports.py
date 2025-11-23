import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_crude_oil_exports(crude_oil_exports_data: dict) -> dict:
    """Parse crude oil exports from CIA Energy section."""
    result = {}
    if not crude_oil_exports_data or not isinstance(crude_oil_exports_data, dict):
        return result
    try:
        if 'text' in crude_oil_exports_data:
            text = crude_oil_exports_data['text']
            if text and isinstance(text, str):
                result['crude_oil_exports'] = clean_text(text)
    except Exception as e:
        logging.error(f"Error parsing crude_oil_exports: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'crude_oil_exports'
    # --------------------------------------------------------------------------------------------------
    # ['crude_oil_exports']
    # --------------------------------------------------------------------------------------------------
    crude_oil_exports_data = {
        "text": "0 bbl/day (2015 est.)"
    }
    parsed_data = parse_crude_oil_exports(crude_oil_exports_data)
    print(parsed_data)
