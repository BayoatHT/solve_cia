import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_phone_mobile_cellular(mobile_cellular_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    mobile_cellular_data = {
        "total subscriptions": {
            "text": "372.682 million (2022 est.)"
        },
        "subscriptions per 100 inhabitants": {
            "text": "110 (2022 est.)"
        }
    }
    parsed_data = parse_phone_mobile_cellular(mobile_cellular_data)
    print(parsed_data)
