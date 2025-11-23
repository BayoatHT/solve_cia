import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_refined_petroleum_consumption(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'refined_petroleum_consumption'
    # --------------------------------------------------------------------------------------------------
    # ['refined_petroleum_consumption']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "1,700 bbl/day (2016 est.)"
    }
    parsed_data = parse_refined_petroleum_consumption(pass_data)
    print(parsed_data)
