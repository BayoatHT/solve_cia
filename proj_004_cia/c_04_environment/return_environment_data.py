"""
PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF ENVIRONMENT INFORMATION FROM THE CIA WORLD FACTBOOK

This module extracts and compiles all 19 environment-related fields from CIA World Factbook data.

Fields extracted:
    - air_pollutants: PM, CO2, methane emissions
    - climate: Climate description and extremes
    - env_current_issues: Environmental issues list
    - env_international_agreements: Treaties and agreements
    - food_insecurity: Food security status
    - geoparks: UNESCO geoparks
    - land_use: Agricultural, forest, other percentages
    - major_aquifers: Underground water sources
    - major_lakes: Fresh and salt water lakes
    - major_rivers: Rivers by length
    - major_watersheds: Watershed areas
    - revenue_from_coal: Coal revenue as % GDP
    - revenue_from_forest: Forest revenue as % GDP
    - total_renewable_water: Renewable water resources
    - total_water_withdrawal: Water usage by sector
    - urbanization: Urban population and growth rate
    - waste_and_recycling: Waste management stats
    - world_biomes: Biome descriptions (World only)
    - marine_fisheries: Ocean fishery data (Oceans only)
"""

import json
import os
from typing import Dict, Optional

from proj_004_cia.c_04_environment.helper.get_environment import get_environment
from proj_004_cia.c_00_transform_utils.clean_output import clean_output


def return_environment_data(data: dict, iso3Code: str) -> Dict:
    """
    Extract and return all environment data for a country.

    Args:
        data: Raw CIA World Factbook JSON data for a country
        iso3Code: ISO3 country code (e.g., 'USA', 'FRA', 'WLD')

    Returns:
        Dictionary containing all 19 environment fields with parsed data
    """
    cia_pack = {}

    # 1. Air pollutants (PM, CO2, methane)
    cia_pack['air_pollutants'] = get_environment(
        data=data, info='air_pollutants', iso3Code=iso3Code)

    # 2. Climate description and extremes
    cia_pack['climate'] = get_environment(
        data=data, info='climate', iso3Code=iso3Code)

    # 3. Environment current issues
    cia_pack['env_current_issues'] = get_environment(
        data=data, info='env_current_issues', iso3Code=iso3Code)

    # 4. International environmental agreements
    cia_pack['env_international_agreements'] = get_environment(
        data=data, info='env_international_agreements', iso3Code=iso3Code)

    # 5. Food insecurity status
    cia_pack['food_insecurity'] = get_environment(
        data=data, info='food_insecurity', iso3Code=iso3Code)

    # 6. Geoparks (UNESCO global geoparks)
    cia_pack['geoparks'] = get_environment(
        data=data, info='geoparks', iso3Code=iso3Code)

    # 7. Land use percentages
    cia_pack['land_use'] = get_environment(
        data=data, info='land_use', iso3Code=iso3Code)

    # 8. Major aquifers
    cia_pack['major_aquifers'] = get_environment(
        data=data, info='major_aquifers', iso3Code=iso3Code)

    # 9. Major lakes (fresh and salt water)
    cia_pack['major_lakes'] = get_environment(
        data=data, info='major_lakes', iso3Code=iso3Code)

    # 10. Major rivers by length
    cia_pack['major_rivers'] = get_environment(
        data=data, info='major_rivers', iso3Code=iso3Code)

    # 11. Major watersheds
    cia_pack['major_watersheds'] = get_environment(
        data=data, info='major_watersheds', iso3Code=iso3Code)

    # 12. Revenue from coal (% of GDP)
    cia_pack['revenue_from_coal'] = get_environment(
        data=data, info='revenue_from_coal', iso3Code=iso3Code)

    # 13. Revenue from forest resources (% of GDP)
    cia_pack['revenue_from_forest'] = get_environment(
        data=data, info='revenue_from_forest', iso3Code=iso3Code)

    # 14. Total renewable water resources
    cia_pack['total_renewable_water'] = get_environment(
        data=data, info='total_renewable_water', iso3Code=iso3Code)

    # 15. Total water withdrawal by sector
    cia_pack['total_water_withdrawal'] = get_environment(
        data=data, info='total_water_withdrawal', iso3Code=iso3Code)

    # 16. Urbanization statistics
    cia_pack['urbanization'] = get_environment(
        data=data, info='urbanization', iso3Code=iso3Code)

    # 17. Waste and recycling statistics
    cia_pack['waste_and_recycling'] = get_environment(
        data=data, info='waste_and_recycling', iso3Code=iso3Code)

    # 18. World biomes (World entity only)
    cia_pack['world_biomes'] = get_environment(
        data=data, info='world_biomes', iso3Code=iso3Code)

    # 19. Marine fisheries (Ocean entities only)
    cia_pack['marine_fisheries'] = get_environment(
        data=data, info='marine_fisheries', iso3Code=iso3Code)

    return clean_output(cia_pack)


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    from pprint import pprint
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    # --------------------------------------------------------------------------------------------------
    # Change to any ISO3 code: 'USA', 'FRA', 'WLD', 'DEU', etc.
    iso3Code = 'NGA'
    # --------------------------------------------------------------------------------------------------
    data = load_country_data(iso3Code)
    # --------------------------------------------------------------------------------------------------
    pprint(return_environment_data(data=data, iso3Code=iso3Code))
