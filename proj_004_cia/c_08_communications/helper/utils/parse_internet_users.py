import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_internet_users(internet_users_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    internet_users_data = {
        "total": {
            "text": "312.8 million (2021 est.)"
        },
        "percent of population": {
            "text": "92% (2021 est.)"
        }
    }
    parsed_data = parse_internet_users(internet_users_data)
    print(parsed_data)
