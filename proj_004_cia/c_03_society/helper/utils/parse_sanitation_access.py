import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_sanitation_access(sanitation_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    sanitation_data = {
        "improved: urban": {
            "text": "urban: 99.8% of population"
        },
        "improved: rural": {
            "text": "rural: 98.9% of population"
        },
        "improved: total": {
            "text": "total: 99.7% of population"
        },
        "unimproved: urban": {
            "text": "urban: 0.2% of population"
        },
        "unimproved: rural": {
            "text": "rural: 11.1% of population"
        },
        "unimproved: total": {
            "text": "total: 0.3% of population (2020 est.)"
        }
    }
    parsed_data = parse_sanitation_access(sanitation_data)
    print(parsed_data)
