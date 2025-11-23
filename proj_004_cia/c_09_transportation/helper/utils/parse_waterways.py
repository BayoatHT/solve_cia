import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_waterways(waterways_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # ['waterways', 'waterways_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    waterways_data = {
        "text": "41,009 km (2012) (19,312 km used for commerce; Saint Lawrence Seaway of 3,769 km, including the Saint Lawrence River of 3,058 km, is shared with Canada)",
        "note": ""
    }
    parsed_data = parse_waterways(waterways_data)
    print(parsed_data)
