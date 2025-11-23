import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_real_gdp_growth_rate(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 35 >>> 'Real GDP growth rate'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Real GDP growth rate 2023": {
            "text": "2.73% (2023 est.)"
        },
        "Real GDP growth rate 2022": {
            "text": "5.49% (2022 est.)"
        },
        "Real GDP growth rate 2021": {
            "text": "11.92% (2021 est.)"
        },
        "note": "<b>note:</b> annual GDP % growth based on constant local currency"
    }
    parsed_data = parse_real_gdp_growth_rate(pass_data)
    print(parsed_data)
