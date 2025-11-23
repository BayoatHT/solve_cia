import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_child_under_5_under_weight(child_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    child_data = {
        "text": "0.4% (2017/18)"
    }
    parsed_data = parse_child_under_5_under_weight(child_data)
    print(parsed_data)
