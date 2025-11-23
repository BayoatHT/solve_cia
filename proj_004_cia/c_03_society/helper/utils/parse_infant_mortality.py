import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_infant_mortality(infant_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    infant_data = {
        "total": {
            "text": "5.1 deaths/1,000 live births (2024 est.)"
        },
        "male": {
            "text": "5.4 deaths/1,000 live births"
        },
        "female": {
            "text": "4.7 deaths/1,000 live births"
        }
    }
    parsed_data = parse_infant_mortality(infant_data)
    print(parsed_data)
