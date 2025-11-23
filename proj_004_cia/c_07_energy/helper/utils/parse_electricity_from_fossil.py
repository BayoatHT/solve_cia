import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_from_fossil(pass_data: dict) -> dict:
    """

    """

    result = {}

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
