import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_airports(airports_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    airports_data = {
        "text": "15,873 (2024)",
        "note": ""
    }
    parsed_data = parse_airports(airports_data)
    print(parsed_data)
