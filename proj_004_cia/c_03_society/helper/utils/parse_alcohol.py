import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_alcohol(alcohol_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    alcohol_data = {
        "total": {
            "text": "8.93 liters of pure alcohol (2019 est.)"
        },
        "beer": {
            "text": "3.97 liters of pure alcohol (2019 est.)"
        },
        "wine": {
            "text": "1.67 liters of pure alcohol (2019 est.)"
        },
        "spirits": {
            "text": "3.29 liters of pure alcohol (2019 est.)"
        },
        "other alcohols": {
            "text": "0 liters of pure alcohol (2019 est.)"
        }
    }
    parsed_data = parse_alcohol(alcohol_data)
    print(parsed_data)
