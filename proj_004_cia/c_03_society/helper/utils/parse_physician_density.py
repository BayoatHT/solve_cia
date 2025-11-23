import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_physician_density(doctor_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    doctor_data = {
        "text": "2.61 physicians/1,000 population (2018)"
    }
    parsed_data = parse_physician_density(doctor_data)
    print(parsed_data)
