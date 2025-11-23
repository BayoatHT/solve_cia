import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_inflation_rate(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 29 >>> 'Inflation rate (consumer prices)'
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # "Inflation rate (consumer prices) 2023" - 'inflation_rate_2023'
    # "note" - 'inflation_rate_note'
    # --------------------------------------------------------------------------------------------------
    # ['inflation_rate_2023', 'inflation_rate_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Inflation rate (consumer prices) 2023": {
            "text": "4.12% (2023 est.)"
        },
        "Inflation rate (consumer prices) 2022": {
            "text": "8% (2022 est.)"
        },
        "Inflation rate (consumer prices) 2021": {
            "text": "4.7% (2021 est.)"
        },
        "note": "<b>note:</b> annual % change based on consumer prices"
    }
    parsed_data = parse_inflation_rate(pass_data)
    print(parsed_data)
