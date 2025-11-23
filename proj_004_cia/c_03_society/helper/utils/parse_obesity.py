import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_obesity(obesity_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    obesity_data = {
        "text": "36.2% (2016)"
    }
    parsed_data = parse_obesity(obesity_data)
    print(parsed_data)
