import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_urbanization(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'env_urbanization_note'
    # "rate of urbanization" - 'env_urbanization_rate'
    # "urban population" - 'env_urbanization_population'
    # --------------------------------------------------------------------------------------------------
    # ['env_urbanization_note', 'env_urbanization_rate', 'env_urbanization_population']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "urban population": {
            "text": "83.3% of total population (2023)"
        },
        "rate of urbanization": {
            "text": "0.96% annual rate of change (2020-25 est.)"
        }
    }
    parsed_data = parse_urbanization(pass_data)
    print(parsed_data)
