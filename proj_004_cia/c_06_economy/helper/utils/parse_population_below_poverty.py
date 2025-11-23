import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_population_below_poverty(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 32 >>> 'Population below poverty line'
    # --------------------------------------------------------------------------------------------------
    # "note" -  'population_below_poverty_line_note'
    # "text" - 'population_below_poverty_line'
    # --------------------------------------------------------------------------------------------------
    # ['population_below_poverty_line', 'population_below_poverty_line_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "16.1% (2015 est.)",
        "note": "<b>note:</b> % of population with income below national poverty line"
    }
    parsed_data = parse_population_below_poverty(pass_data)
    print(parsed_data)
