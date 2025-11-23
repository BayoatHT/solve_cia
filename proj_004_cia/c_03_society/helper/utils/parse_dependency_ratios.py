import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_dependency_ratios(dependency_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    dependency_data = {
        "total dependency ratio": {
            "text": "53.7"
        },
        "youth dependency ratio": {
            "text": "28"
        },
        "elderly dependency ratio": {
            "text": "25.6"
        },
        "potential support ratio": {
            "text": "3.9 (2021 est.)"
        }
    }
    parsed_data = parse_dependency_ratios(dependency_data)
    print(parsed_data)
