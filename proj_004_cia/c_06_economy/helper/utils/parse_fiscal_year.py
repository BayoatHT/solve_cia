import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_fiscal_year(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 15 >>> 'Fiscal year'
    # --------------------------------------------------------------------------------------------------
    # text - 'fiscal_year'
    # --------------------------------------------------------------------------------------------------
    # ['fiscal_year']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "calendar year"
    }
    parsed_data = parse_fiscal_year(pass_data)
    print(parsed_data)
