import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ports_and_terminals(ports_and_terminals_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # major seaport(s) - major_seaports
    # --------------------------------------------------------------------------------------------------
    # ['major_seaports']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    ports_and_terminals_data = {
        "major seaport(s)": {
            "text": "Ad Dakhla, Laayoune (El Aaiun)"
        }
    }
    parsed_data = parse_ports_and_terminals(ports_and_terminals_data)
    print(parsed_data)
