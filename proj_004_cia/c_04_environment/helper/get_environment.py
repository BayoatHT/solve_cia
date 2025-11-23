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


if __name__ == '__main__':
    from pathlib import Path
    from pprint import pprint

    # Configuration
    TEST_INFO = 'climate'  # Change to test different fields
    TEST_COUNTRY = 'USA'   # Options: 'USA', 'FRA', 'WLD'

    # Determine paths based on platform
    if os.name == 'nt':  # Windows
        json_folder = Path(r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data')
    else:  # Linux/Mac
        json_folder = Path(__file__).parent.parent.parent / '_raw_data'

    # Country configuration
    country_config = {
        'USA': ('north-america', 'us'),
        'FRA': ('europe', 'fr'),
        'WLD': ('world', 'xx'),
    }

    region_folder, cia_code = country_config.get(TEST_COUNTRY, ('north-america', 'us'))
    file_path = json_folder / region_folder / f'{cia_code}.json'

    print(f"Loading: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\n{'='*60}")
    print(f"TESTING: get_environment(info='{TEST_INFO}')")
    print(f"COUNTRY: {TEST_COUNTRY}")
    print(f"{'='*60}\n")

    result = get_environment(data=data, info=TEST_INFO, iso3Code=TEST_COUNTRY)
    pprint(result, width=100)

    # Test all fields
    print(f"\n{'='*60}")
    print("TESTING ALL FIELDS")
    print(f"{'='*60}")
    for field in sorted(VALID_INFO_PARAMS):
        result = get_environment(data=data, info=field, iso3Code=TEST_COUNTRY)
        has_data = result is not None and any(
            v for v in (result.values() if isinstance(result, dict) else [result])
            if v is not None and v != [] and v != {} and v != ''
        )
        status = "✓" if has_data else "-"
        print(f"  {status} {field}")
