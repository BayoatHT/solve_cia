import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_petroleum(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "crude oil estimated reserves" - 'crude_oil_estimated_reserves'
    # "note" - 'petroleum_note'
    # "refined petroleum consumption" - 'refined_petroleum_consumption'
    # "total petroleum production" - 'total_petroleum_production'
    # --------------------------------------------------------------------------------------------------
    # ['crude_oil_estimated_reserves', 'petroleum_note', 'refined_petroleum_consumption',
    # 'total_petroleum_production']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "total petroleum production": {
            "text": "20.879 million bbl/day (2023 est.)"
        },
        "refined petroleum consumption": {
            "text": "20.246 million bbl/day (2023 est.)"
        },
        "crude oil estimated reserves": {
            "text": "38.212 billion barrels (2021 est.)"
        }
    }
    parsed_data = parse_petroleum(pass_data)
    print(parsed_data)
