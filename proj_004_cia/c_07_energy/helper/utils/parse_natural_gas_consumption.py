import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_natural_gas_consumption(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'natural_gas_consumption'
    # --------------------------------------------------------------------------------------------------
    # ['natural_gas_consumption']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 cu m (2017 est.)"
    }
    parsed_data = parse_natural_gas_consumption(pass_data)
    print(parsed_data)
