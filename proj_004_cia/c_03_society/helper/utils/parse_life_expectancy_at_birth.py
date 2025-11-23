import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_life_expectancy_at_birth(life_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    life_data = {
        "total population": {
            "text": "80.9 years (2024 est.)"
        },
        "male": {
            "text": "78.7 years"
        },
        "female": {
            "text": "83.1 years"
        }
    }
    parsed_data = parse_life_expectancy_at_birth(life_data)
    print(parsed_data)
