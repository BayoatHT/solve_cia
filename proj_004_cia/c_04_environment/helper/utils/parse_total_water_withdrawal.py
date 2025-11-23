import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_total_water_withdrawal(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "agricultural" - 'env_water_withdrawal_agricultural'
    # "industrial" - 'env_water_withdrawal_industrial'
    # "municipal" - 'env_water_withdrawal_municipal'
    # "note" - 'env_water_withdrawal_note'
    # --------------------------------------------------------------------------------------------------
    # ['env_water_withdrawal_agricultural', 'env_water_withdrawal_industrial',
    # 'env_water_withdrawal_municipal', 'env_water_withdrawal_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "municipal": {
            "text": "58.39 billion cubic meters (2020 est.)"
        },
        "industrial": {
            "text": "209.7 billion cubic meters (2020 est.)"
        },
        "agricultural": {
            "text": "176.2 billion cubic meters (2020 est.)"
        },
        "note": ""
    }
    parsed_data = parse_total_water_withdrawal(pass_data)
    print(parsed_data)
