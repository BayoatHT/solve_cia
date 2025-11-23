import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_real_gdp_ppp(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 34 >>> 'Real GDP (purchasing power parity)'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Real GDP (purchasing power parity) 2023": {
            "text": "$46.742 billion (2023 est.)"
        },
        "Real GDP (purchasing power parity) 2022": {
            "text": "$45.499 billion (2022 est.)"
        },
        "Real GDP (purchasing power parity) 2021": {
            "text": "$43.133 billion (2021 est.)"
        },
        "note": "<b>note:</b> data in 2021 dollars"
    }
    parsed_data = parse_real_gdp_ppp(pass_data)
    print(parsed_data)
