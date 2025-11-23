import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_education_expenditure(education_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    education_data = {
        "text": "6.1% of GDP (2020 est.)"
    }
    parsed_data = parse_education_expenditure(education_data)
    print(parsed_data)
