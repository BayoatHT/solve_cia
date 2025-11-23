import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_total_renewable_water(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'env_renewable_water_resources_note'
    # "text" - 'env_renewable_water_resources'
    # --------------------------------------------------------------------------------------------------
    # ['env_renewable_water_resources_note', 'env_renewable_water_resources']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "3.07 trillion cubic meters (2020 est.)",
        "note": ""
    }
    parsed_data = parse_total_renewable_water(pass_data)
    print(parsed_data)
