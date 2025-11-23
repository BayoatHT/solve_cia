import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_exports(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 12 >>> 'Exports'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Exports 2023": {
            "text": "$3.052 trillion (2023 est.)"
        },
        "Exports 2022": {
            "text": "$3.018 trillion (2022 est.)"
        },
        "Exports 2021": {
            "text": "$2.567 trillion (2021 est.)"
        },
        "note": "<strong>note:</strong> balance of payments - exports of goods and services in current dollars"
    }
    parsed_data = parse_exports(pass_data)
    print(parsed_data)
