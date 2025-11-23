import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_transportation_note(transportation_note_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    transportation_note_data = {
        "text": ""
    }
    parsed_data = parse_transportation_note(transportation_note_data)
    print(parsed_data)
