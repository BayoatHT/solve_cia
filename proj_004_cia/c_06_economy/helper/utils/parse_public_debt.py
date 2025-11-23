import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_public_debt(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 33 >>> 'Public debt'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Public debt 2020": {
            "text": "19.62% of GDP (2020 est.)"
        },
        "note": "<b>note:</b> central government debt as a % of GDP"
    }
    parsed_data = parse_public_debt(pass_data)
    print(parsed_data)
