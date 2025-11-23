import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_civil_reg_code(civil_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # ['civil_reg_code']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    civil_data = {
        "text": "F"
    }
    parsed_data = parse_civil_reg_code(civil_data)
    print(parsed_data)
