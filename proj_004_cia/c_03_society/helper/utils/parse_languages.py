import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_languages(languages_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    languages_data = {
        "text": "English only 78.2%, Spanish 13.4%, Chinese 1.1%, other 7.3% (2017 est.)",
        "note": "<strong>note:</strong> data represent the language spoken at home; the US has no official national language, but English has acquired official status in 32 of the 50 states; Hawaiian is an official language in the state of Hawaii, and 20 indigenous languages are official in Alaska"
    }
    parsed_data = parse_languages(languages_data)
    print(parsed_data)
