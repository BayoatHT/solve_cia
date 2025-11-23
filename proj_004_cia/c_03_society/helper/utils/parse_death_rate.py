import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_death_rate(death_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    death_data = {
        "text": "8.5 deaths/1,000 population (2024 est.)"
    }
    parsed_data = parse_death_rate(death_data)
    print(parsed_data)
