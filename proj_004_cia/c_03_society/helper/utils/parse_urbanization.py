import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_urbanization(urb_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    urb_data = {
        "urban population": {
            "text": "83.3% of total population (2023)"
        },
        "rate of urbanization": {
            "text": "0.96% annual rate of change (2020-25 est.)"
        }
    }
    parsed_data = parse_urbanization(urb_data)
    print(parsed_data)
