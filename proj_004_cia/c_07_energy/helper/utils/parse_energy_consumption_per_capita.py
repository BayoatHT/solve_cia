import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_energy_consumption_per_capita(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # GET MORE FROM WORLD BANK
    # "Total energy consumption per capita 2022" - 'energy_consumption_per_capita_2022'
    # "note" - 'energy_consumption_per_capita_note'
    # --------------------------------------------------------------------------------------------------
    # ['energy_consumption_per_capita_2022', 'energy_consumption_per_capita_note']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Total energy consumption per capita 2022": {
            "text": "284.575 million Btu/person (2022 est.)"
        }
    }
    parsed_data = parse_energy_consumption_per_capita(pass_data)
    print(parsed_data)
