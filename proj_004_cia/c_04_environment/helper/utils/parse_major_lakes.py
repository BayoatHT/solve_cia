import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_lakes(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "fresh water lake(s)" - 'env_major_lakes_fresh'
    # "salt water lake(s)" - 'env_major_lakes_salt'
    # --------------------------------------------------------------------------------------------------
    # ['env_major_lakes_fresh', 'env_major_lakes_salt']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {

    }
    parsed_data = parse_major_lakes(pass_data)
    print(parsed_data)
