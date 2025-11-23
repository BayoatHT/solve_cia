import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_imports_commodities(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 25 >>> 'Imports - commodities'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'imports_commodities_note'
    # "text" - 'imports_commodities'
    # --------------------------------------------------------------------------------------------------
    # ['imports_commodities', 'imports_commodities_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "crude petroleum, cars, broadcasting equipment, garments, computers (2022)",
        "note": "<b>note:</b> top five import commodities based on value in dollars"
    }
    parsed_data = parse_imports_commodities(pass_data)
    print(parsed_data)
