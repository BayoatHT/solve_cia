import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_food_insecurity(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "exceptional shortfall in aggregate food production/supplies" - 'env_food_insecurity_exceptional'
    # "severe localized food insecurity" - 'env_food_insecurity_severe'
    # "widespread lack of access" - 'env_food_insecurity_widespread'
    # --------------------------------------------------------------------------------------------------
    # ['env_food_insecurity_exceptional', 'env_food_insecurity_severe', 'env_food_insecurity_widespread']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {

    }
    parsed_data = parse_food_insecurity(pass_data)
    print(parsed_data)
