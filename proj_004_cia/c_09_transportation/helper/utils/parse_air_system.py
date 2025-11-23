import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_air_system(air_system_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # [ 'annual_freight', 'annual_passenger', 'inventory_aircraft', 'num_reg_aircraft']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    air_system_data = {
        "number of registered air carriers": {
            "text": "19 (2020)"
        },
        "inventory of registered aircraft operated by air carriers": {
            "text": "553"
        },
        "annual passenger traffic on registered air carriers": {
            "text": "70,188,028 (2018)"
        },
        "annual freight traffic on registered air carriers": {
            "text": "4,443,790,000 (2018) mt-km"
        }
    }
    parsed_data = parse_air_system(air_system_data)
    print(parsed_data)
