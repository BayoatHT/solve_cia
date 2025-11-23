import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_imports(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'electricity_imports'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_imports']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 kWh (2016 est.)"
    }
    parsed_data = parse_electricity_imports(pass_data)
    print(parsed_data)
