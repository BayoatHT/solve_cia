import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_airports_paved(airports_paved_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":

    airports_paved_data = {
        "total": {
            "text": "3 (2019)"
        },
        "2,438 to 3,047 m": {
            "text": "3"
        }
    }
    parsed_data = parse_airports_paved(airports_paved_data)
    print(parsed_data)
