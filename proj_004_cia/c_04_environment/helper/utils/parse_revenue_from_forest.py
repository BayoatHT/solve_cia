import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_revenue_from_forest(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'env_revenue_forest_resources'
    # --------------------------------------------------------------------------------------------------
    # ['env_revenue_forest_resources']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "0.04% of GDP (2018 est.)"
    }
    parsed_data = parse_revenue_from_forest(pass_data)
    print(parsed_data)
