import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_tobacco_use(tobacco_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    tobacco_data = {
        "total": {
            "text": "23% (2020 est.)"
        },
        "male": {
            "text": "28.4% (2020 est.)"
        },
        "female": {
            "text": "17.5% (2020 est.)"
        }
    }
    parsed_data = parse_tobacco_use(tobacco_data)
    print(parsed_data)
