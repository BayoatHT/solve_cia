import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_phone_fixed_lines(phone_fixed_lines_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    phone_fixed_lines_data = {
        "total subscriptions": {
            "text": "91.623 million (2022 est.)"
        },
        "subscriptions per 100 inhabitants": {
            "text": "27 (2022 est.)"
        },
        "note": ""
    }
    parsed_data = parse_phone_fixed_lines(phone_fixed_lines_data)
    print(parsed_data)
