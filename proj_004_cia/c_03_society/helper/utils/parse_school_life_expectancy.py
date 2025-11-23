import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_school_life_expectancy(school_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    school_data = {
        "total": {
            "text": "16 years"
        },
        "male": {
            "text": "16 years"
        },
        "female": {
            "text": "17 years (2020)"
        }
    }
    parsed_data = parse_school_life_expectancy(school_data)
    print(parsed_data)
