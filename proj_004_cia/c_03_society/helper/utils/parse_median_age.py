import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_median_age(median_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    median_data = {
        "total": {
            "text": "38.9 years (2022 est.)"
        },
        "male": {
            "text": "37.8 years"
        },
        "female": {
            "text": "40 years"
        }
    }
    parsed_data = parse_median_age(median_data)
    print(parsed_data)
