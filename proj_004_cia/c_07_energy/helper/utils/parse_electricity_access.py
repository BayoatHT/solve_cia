import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_access(electricity_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "electrification - rural areas" - 'electricity_access_rural_areas'
    # "electrification - total population" - 'electricity_access_total_population'
    # "electrification - urban areas" - 'electricity_access_urban_areas'
    # "note" - 'electricity_access_note'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_access_rural_areas', 'electricity_access_total_population',
    # 'electricity_access_urban_areas', 'electricity_access_note']
    electricity_data = {
        "electrification - total population": {
            "text": "100% (2022 est.)"
        },
        "electrification - urban areas": {
            "text": "100%"
        },
        "electrification - rural areas": {
            "text": "99.3%"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_electricity_access(electricity_data)
    print(parsed_data)
