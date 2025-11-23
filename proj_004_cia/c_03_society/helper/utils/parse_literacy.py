import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_literacy(literacy_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    literacy_data = {
        "total population": {
            "text": "NA"
        },
        "male": {
            "text": "NA"
        },
        "female": {
            "text": "NA"
        }
    }
    parsed_data = parse_literacy(literacy_data)
    print(parsed_data)
