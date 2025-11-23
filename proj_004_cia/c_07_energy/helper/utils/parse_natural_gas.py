import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_natural_gas(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    # text - 'natural_gas'
    # --------------------------------------------------------------------------------------------------
    # ['natural_gas']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "production": {
            "text": "1.029 trillion cubic meters (2022 est.)"
        },
        "consumption": {
            "text": "914.301 billion cubic meters (2022 est.)"
        },
        "exports": {
            "text": "195.497 billion cubic meters (2022 est.)"
        },
        "imports": {
            "text": "85.635 billion cubic meters (2022 est.)"
        },
        "proven reserves": {
            "text": "13.402 trillion cubic meters (2021 est.)"
        }
    }
    parsed_data = parse_natural_gas(pass_data)
    print(parsed_data)
