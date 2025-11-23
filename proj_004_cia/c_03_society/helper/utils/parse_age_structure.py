import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# proj_004_cia.c_00_transform_utils
# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_age_structure(age_structure_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    age_structure_data = {
        "0-14 years": {
            "text": "18.1% (male 31,618,532/female 30,254,223)"
        },
        "15-64 years": {
            "text": "63.4% (male 108,553,822/female 108,182,491)"
        },
        "65 years and over": {
            "text": "18.5% (2024 est.) (male 28,426,426/female 34,927,914)"
        }
    }
    parsed_data = parse_age_structure(age_structure_data)
    print(parsed_data)
