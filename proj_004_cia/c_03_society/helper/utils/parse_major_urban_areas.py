import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_urban_areas(major_urban_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    major_urban_data = {
        "text": "18.937 million New York-Newark, 12.534 million Los Angeles-Long Beach-Santa Ana, 8.937 million Chicago, 6.707 million Houston, 6.574 million Dallas-Fort Worth, 5.490 million WASHINGTON, D.C. (capital) (2023)"
    }
    parsed_data = parse_major_urban_areas(major_urban_data)
    print(parsed_data)
