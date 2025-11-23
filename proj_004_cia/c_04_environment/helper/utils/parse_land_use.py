import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_land_use(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "agricultural land" - 'env_land_use_agricultural'
    # "agricultural land: arable land" - 'env_land_use_agricultural_arable'
    # "agricultural land: permanent crops" - 'env_land_use_agricultural_perm_crops'
    # "agricultural land: permanent pasture" - 'env_land_use_agricultural_perm_pasture'
    # "forest" - 'env_land_use_forest'
    # "note" - 'env_land_use_note'
    # "other" - 'env_land_use_other'
    # --------------------------------------------------------------------------------------------------
    # ['env_land_use_agricultural', 'env_land_use_agricultural_arable', 'env_land_use_agricultural_perm_crops',
    # 'env_land_use_agricultural_perm_pasture', 'env_land_use_forest', 'env_land_use_note', 'env_land_use_other']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "agricultural land": {
            "text": "44.5% (2018 est.)"
        },
        "agricultural land: arable land": {
            "text": "arable land: 16.8% (2018 est.)"
        },
        "agricultural land: permanent crops": {
            "text": "permanent crops: 0.3% (2018 est.)"
        },
        "agricultural land: permanent pasture": {
            "text": "permanent pasture: 27.4% (2018 est.)"
        },
        "forest": {
            "text": "33.3% (2018 est.)"
        },
        "other": {
            "text": "22.2% (2018 est.)"
        }
    }
    parsed_data = parse_land_use(pass_data)
    print(parsed_data)
