import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_air_pollutants(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "carbon dioxide emissions" - 'env_air_pollutants_co2_emissions'
    # "methane emissions" - 'env_air_pollutants_methane_emissions'
    # "note" - 'env_air_pollutants_note'
    # "particulate matter emissions" - 'env_air_pollutants_particulate_emissions'
    # --------------------------------------------------------------------------------------------------
    # ['env_air_pollutants_co2_emissions', 'env_air_pollutants_methane_emissions',
    # 'env_air_pollutants_note', 'env_air_pollutants_particulate_emissions']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "particulate matter emissions": {
            "text": "7.18 micrograms per cubic meter (2019 est.)"
        },
        "carbon dioxide emissions": {
            "text": "5,006.3 megatons (2016 est.)"
        },
        "methane emissions": {
            "text": "685.74 megatons (2020 est.)"
        },
        "note": ""
    },
    parsed_data = parse_air_pollutants(pass_data)
    print(parsed_data)
