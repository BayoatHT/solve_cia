import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_waste_and_recycling(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # "municipal solid waste generated annually" - 'env_waste_recycling_generated'
    # "municipal solid waste recycled annually" - 'env_waste_recycling_recycled'
    # "note" - 'env_waste_recycling_note'
    # "percent of municipal solid waste recycled" - 'env_waste_recycling_percent'
    # --------------------------------------------------------------------------------------------------
    # ['env_waste_recycling_generated', 'env_waste_recycling_recycled',
    # 'env_waste_recycling_note', 'env_waste_recycling_percent']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "municipal solid waste generated annually": {
            "text": "258 million tons (2015 est.)"
        },
        "municipal solid waste recycled annually": {
            "text": "89.268 million tons (2014 est.)"
        },
        "percent of municipal solid waste recycled": {
            "text": "34.6% (2014 est.)"
        }
    }
    parsed_data = parse_waste_and_recycling(pass_data)
    print(parsed_data)
