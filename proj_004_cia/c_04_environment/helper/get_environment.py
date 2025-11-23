"""
Environment Data Router

Routes environment field requests to appropriate parsers.
Supports 19 environment fields from CIA World Factbook.

Usage:
    result = get_environment(data=country_data, info='climate', iso3Code='USA')
"""

import os
import json
from typing import Dict, Optional

# Parser imports
from proj_004_cia.c_04_environment.helper.utils.parse_air_pollutants import parse_air_pollutants
from proj_004_cia.c_04_environment.helper.utils.parse_climate import parse_climate
from proj_004_cia.c_04_environment.helper.utils.parse_env_current_issues import parse_env_current_issues
from proj_004_cia.c_04_environment.helper.utils.parse_env_international_agreements import parse_env_international_agreements
from proj_004_cia.c_04_environment.helper.utils.parse_food_insecurity import parse_food_insecurity
from proj_004_cia.c_04_environment.helper.utils.parse_geoparks import parse_geoparks
from proj_004_cia.c_04_environment.helper.utils.parse_land_use import parse_land_use
from proj_004_cia.c_04_environment.helper.utils.parse_major_aquifers import parse_major_aquifers
from proj_004_cia.c_04_environment.helper.utils.parse_major_lakes import parse_major_lakes
from proj_004_cia.c_04_environment.helper.utils.parse_major_rivers import parse_major_rivers
from proj_004_cia.c_04_environment.helper.utils.parse_major_watersheds import parse_major_watersheds
from proj_004_cia.c_04_environment.helper.utils.parse_revenue_from_coal import parse_revenue_from_coal
from proj_004_cia.c_04_environment.helper.utils.parse_revenue_from_forest import parse_revenue_from_forest
from proj_004_cia.c_04_environment.helper.utils.parse_total_renewable_water import parse_total_renewable_water
from proj_004_cia.c_04_environment.helper.utils.parse_total_water_withdrawal import parse_total_water_withdrawal
from proj_004_cia.c_04_environment.helper.utils.parse_urbanization import parse_urbanization
from proj_004_cia.c_04_environment.helper.utils.parse_waste_and_recycling import parse_waste_and_recycling
from proj_004_cia.c_04_environment.helper.utils.parse_world_biomes import parse_world_biomes
from proj_004_cia.c_04_environment.helper.utils.parse_marine_fisheries import parse_marine_fisheries


# Valid info parameters
VALID_INFO_PARAMS = {
    'air_pollutants',
    'climate',
    'env_current_issues',
    'env_international_agreements',
    'food_insecurity',
    'geoparks',
    'land_use',
    'major_aquifers',
    'major_lakes',
    'major_rivers',
    'major_watersheds',
    'revenue_from_coal',
    'revenue_from_forest',
    'total_renewable_water',
    'total_water_withdrawal',
    'urbanization',
    'waste_and_recycling',
    'world_biomes',
    'marine_fisheries',
}


def get_environment(data: dict = None, info: str = None, iso3Code: str = None) -> Optional[Dict]:
    """
    Route environment data requests to the appropriate parser.

    Args:
        data: Raw CIA World Factbook JSON data for a country
        info: Field name to extract (e.g., 'climate', 'air_pollutants')
        iso3Code: ISO3 country code for logging purposes

    Returns:
        Parsed data dictionary for the requested field, or None if invalid info

    Raises:
        ValueError: If info parameter is not recognized
    """
    if data is None:
        return None

    if info is None or info not in VALID_INFO_PARAMS:
        return None

    # Get Environment section
    env_data = data.get("Environment", {})

    # Route to appropriate parser
    if info == 'air_pollutants':
        return parse_air_pollutants(
            env_data.get("Air pollutants", {}),
            iso3Code
        )

    if info == 'climate':
        return parse_climate(
            env_data.get("Climate", {}),
            iso3Code
        )

    if info == 'env_current_issues':
        return parse_env_current_issues(
            env_data.get("Environment - current issues", {}),
            iso3Code
        )

    if info == 'env_international_agreements':
        return parse_env_international_agreements(
            env_data.get("Environment - international agreements", {}),
            iso3Code
        )

    if info == 'food_insecurity':
        return parse_food_insecurity(
            env_data.get("Food insecurity", {}),
            iso3Code
        )

    if info == 'geoparks':
        return parse_geoparks(
            env_data.get("Geoparks", {}),
            iso3Code
        )

    if info == 'land_use':
        return parse_land_use(
            env_data.get("Land use", {}),
            iso3Code
        )

    if info == 'major_aquifers':
        return parse_major_aquifers(
            env_data.get("Major aquifers", {}),
            iso3Code
        )

    if info == 'major_lakes':
        return parse_major_lakes(
            env_data.get("Major lakes (area sq km)", {}),
            iso3Code
        )

    if info == 'major_rivers':
        return parse_major_rivers(
            env_data.get("Major rivers (by length in km)", {}),
            iso3Code
        )

    if info == 'major_watersheds':
        return parse_major_watersheds(
            env_data.get("Major watersheds (area sq km)", {}),
            iso3Code
        )

    if info == 'revenue_from_coal':
        return parse_revenue_from_coal(
            env_data.get("Revenue from coal", {}),
            iso3Code
        )

    if info == 'revenue_from_forest':
        return parse_revenue_from_forest(
            env_data.get("Revenue from forest resources", {}),
            iso3Code
        )

    if info == 'total_renewable_water':
        return parse_total_renewable_water(
            env_data.get("Total renewable water resources", {}),
            iso3Code
        )

    if info == 'total_water_withdrawal':
        return parse_total_water_withdrawal(
            env_data.get("Total water withdrawal", {}),
            iso3Code
        )

    if info == 'urbanization':
        return parse_urbanization(
            env_data.get("Urbanization", {}),
            iso3Code
        )

    if info == 'waste_and_recycling':
        return parse_waste_and_recycling(
            env_data.get("Waste and recycling", {}),
            iso3Code
        )

    if info == 'world_biomes':
        return parse_world_biomes(
            env_data.get("World biomes", {}),
            iso3Code
        )

    if info == 'marine_fisheries':
        return parse_marine_fisheries(
            env_data.get("Marine fisheries", {}),
            iso3Code
        )

    return None


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    from pprint import pprint
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    # --------------------------------------------------------------------------------------------------
    info = 'pass'  # Change this to test specific fields
    iso3Code = 'USA'  # Change to any ISO3 code: 'USA', 'FRA', 'WLD', 'DEU', etc.
    # --------------------------------------------------------------------------------------------------
    data = load_country_data(iso3Code)
    # --------------------------------------------------------------------------------------------------
    pprint(get_environment(data=data, info=info, iso3Code=iso3Code))
