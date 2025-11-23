import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_merchant_marine(merchant_marine_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # ['merchant_marine_total', 'merchant_marine_by_type', 'merchant_marine_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    merchant_marine_data = {
        "total": {
            "text": "3,533 (2023)"
        },
        "by type": {
            "text": "bulk carrier 4, container ship 60, general cargo 96, oil tanker 68, other 3,305"
        },
        "note": "note - oceangoing self-propelled, cargo-carrying vessels of 1,000 gross tons and above"
    }
    parsed_data = parse_merchant_marine(merchant_marine_data)
    print(parsed_data)
