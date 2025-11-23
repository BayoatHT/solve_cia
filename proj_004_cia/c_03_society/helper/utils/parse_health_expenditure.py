import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_health_expenditure(health_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    health_data = {
        "text": "18.8% of GDP (2020)"
    }
    parsed_data = parse_health_expenditure(health_data)
    print(parsed_data)
