import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_sex_ratio(sex_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    sex_data = {
        "at birth": {
            "text": "1.05 male(s)/female"
        },
        "0-14 years": {
            "text": "1.05 male(s)/female"
        },
        "15-64 years": {
            "text": "1 male(s)/female"
        },
        "65 years and over": {
            "text": "0.81 male(s)/female"
        },
        "total population": {
            "text": "0.97 male(s)/female (2024 est.)"
        }
    }
    parsed_data = parse_sex_ratio(sex_data)
    print(parsed_data)
