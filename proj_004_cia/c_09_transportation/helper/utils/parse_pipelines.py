import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_pipelines(pipelines_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # ["pipelines"]
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    pipelines_data = {
        "text": "1,984,321 km natural gas, 240,711 km petroleum products (2013)"
    }
    parsed_data = parse_pipelines(pipelines_data)
    print(parsed_data)
