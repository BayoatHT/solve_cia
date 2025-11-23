import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_real_gdp_per_capita(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 36 >>> 'Real GDP per capita'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Real GDP per capita 2023": {
            "text": "$17,500 (2023 est.)"
        },
        "Real GDP per capita 2022": {
            "text": "$17,300 (2022 est.)"
        },
        "Real GDP per capita 2021": {
            "text": "$16,700 (2021 est.)"
        },
        "note": "<b>note:</b> data in 2021 dollars"
    }
    parsed_data = parse_real_gdp_per_capita(pass_data)
    print(parsed_data)
