import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_airports_unpaved(airports_unpaved_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    #  ['unpaved_runways_total', 'unpaved_runways_0_1', 'unpaved_runways_1_2', 'unpaved_runways_under_914_m']
    # ----------------------------------------------------------------------------------------------------
    airports_unpaved_data = {
        "total": {
            "text": "3 (2013)"
        },
        "1,524 to 2,437 m": {
            "text": "1 (2013)"
        },
        "914 to 1,523 m": {
            "text": "1 (2013)"
        },
        "under 914 m": {
            "text": "1 (2013)"
        }
    }
    parsed_data = parse_airports_unpaved(airports_unpaved_data)
    print(parsed_data)
