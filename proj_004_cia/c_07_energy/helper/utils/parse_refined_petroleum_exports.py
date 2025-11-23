import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_refined_petroleum_exports(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'refined_petroleum_exports'
    # --------------------------------------------------------------------------------------------------
    # [ 'refined_petroleum_exports' ]
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0 bbl/day (2015 est.)"
    }
    parsed_data = parse_refined_petroleum_exports(pass_data)
    print(parsed_data)
