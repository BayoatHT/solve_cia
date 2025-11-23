import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_gdp_official_exchange(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 16 >>> 'GDP (official exchange rate)'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "$27.361 trillion (2023 est.)",
        "note": "<b>note:</b> data in current dollars at official exchange rate"
    }
    parsed_data = parse_gdp_official_exchange(pass_data)
    print(parsed_data)
