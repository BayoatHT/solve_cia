import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_labor_force(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 30 >>> 'Labor force'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'labor_force_note'
    # "text" - 'labor_force'
    # --------------------------------------------------------------------------------------------------
    # ['labor_force', 'labor_force_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "144,000 (2010 est.)"
    }
    parsed_data = parse_labor_force(pass_data)
    print(parsed_data)
