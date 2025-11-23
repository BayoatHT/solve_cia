import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity_sources(electricity_sources_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "biomass and waste" - 'electricity_generation_biomass_waste'
    # "fossil fuels" - 'electricity_generation_fossil_fuels'
    # "geothermal" - 'electricity_generation_geothermal'
    # "hydroelectricity" - 'electricity_generation_hydroelectricity'
    # "note" - 'electricity_generation_note'
    # "nuclear" - 'electricity_generation_nuclear'
    # "solar" - 'electricity_generation_solar'
    # "tide and wave" - 'electricity_generation_tide_wave'
    # "wind" - 'electricity_generation_wind'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_generation_biomass_waste', 'electricity_generation_fossil_fuels',
    # 'electricity_generation_geothermal', 'electricity_generation_hydroelectricity',
    # 'electricity_generation_note', 'electricity_generation_nuclear', 'electricity_generation_solar',
    # 'electricity_generation_tide_wave', 'electricity_generation_wind']
    # --------------------------------------------------------------------------------------------------
    electricity_sources_data = {
        "fossil fuels": {
            "text": "59.5% of total installed capacity (2022 est.)"
        },
        "nuclear": {
            "text": "18% of total installed capacity (2022 est.)"
        },
        "solar": {
            "text": "4.8% of total installed capacity (2022 est.)"
        },
        "wind": {
            "text": "10.1% of total installed capacity (2022 est.)"
        },
        "hydroelectricity": {
            "text": "5.8% of total installed capacity (2022 est.)"
        },
        "geothermal": {
            "text": "0.4% of total installed capacity (2022 est.)"
        },
        "biomass and waste": {
            "text": "1.5% of total installed capacity (2022 est.)"
        }
    }
    parsed_data = parse_electricity_sources(electricity_sources_data)
    print(parsed_data)
