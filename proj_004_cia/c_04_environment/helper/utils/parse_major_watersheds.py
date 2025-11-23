import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_watersheds(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'env_major_watersheds'
    # --------------------------------------------------------------------------------------------------
    # ['env_major_watersheds']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "Atlantic Ocean drainage: <em>(Gulf of Mexico) </em>Mississippi* (3,202,185 sq km); Rio Grande (607,965 sq km); <em>(Gulf of Saint Lawrence)</em> Saint Lawrence* (1,049,636 sq km total, US only 505,000 sq km)<br>Pacific Ocean drainage: Yukon* (847,620 sq km, US only 23,820 sq km); Colorado (703,148 sq km); Columbia* (657,501 sq km, US only 554,501 sq km)<br>note - watersheds shared with Canada shown with *"
    }
    parsed_data = parse_major_watersheds(pass_data)
    print(parsed_data)
