"""
ISO3 Code to CIA Code Mapping and Data Loading Utility.

This module provides functions to:
1. Map ISO3 codes to CIA codes and region names
2. Load raw CIA World Factbook data by ISO3 code

Usage:
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    data = load_country_data('USA')  # Load United States data
    data = load_country_data('FRA')  # Load France data
    data = load_country_data('WLD')  # Load World data
"""

import os
import json
import platform
from typing import Dict, Any, Optional

from proj_004_cia.a_02_cia_area_codes.utils.cia_code_names import cia_code_names

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   REGION NAME TO FOLDER MAPPING
# ---------------------------------------------------------------------------------------------------------------------
REGION_TO_FOLDER = {
    'Africa': 'africa',
    'Antarctica': 'antarctica',
    'Australia-Oceania': 'australia-oceania',
    'Central America and Caribbean': 'central-america-n-caribbean',
    'Central Asia': 'central-asia',
    'East and Southeast Asia': 'east-n-southeast-asia',
    'Europe': 'europe',
    'europe': 'europe',
    'Meta': 'meta',
    'Middle East': 'middle-east',
    'North America': 'north-america',
    'Oceans': 'oceans',
    'South America': 'south-america',
    'South Asia': 'south-asia',
    'World': 'world',
    'world': 'world',
}

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION - ISO3 TO CIA CODE MAPPING
# ---------------------------------------------------------------------------------------------------------------------


def iso3Code_to_cia_code() -> Dict[str, Dict[str, str]]:
    """
    Maps each ISO3 code in cia_code_names to a dictionary with 'region_name' and 'cia_code'.

    Returns:
        dict: A dictionary where keys are ISO3 codes, and values are dictionaries with 'region_name' and 'cia_code'.
    """
    iso3_to_cia = {}

    for parent_key, details in cia_code_names.items():
        iso3_code = details.get("iso3Code")
        region_name = details.get("region_name")
        country_name = details.get("country_name")
        if iso3_code:
            # Get the folder name for the region
            region_folder = REGION_TO_FOLDER.get(region_name, region_name.lower() if region_name else '')
            iso3_to_cia[iso3_code] = {
                "country_name": country_name,
                "region_name": region_name,
                "region_folder": region_folder,
                "cia_code": parent_key
            }

    return iso3_to_cia


# Pre-build the mapping at module load time for performance
ISO3_TO_CIA = iso3Code_to_cia_code()


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   DATA LOADING FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------


def get_raw_data_folder() -> str:
    """
    Get the path to the raw data folder based on the platform.

    Returns:
        str: Path to the _raw_data folder
    """
    if platform.system() == 'Windows':
        return r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    else:
        return os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            '_raw_data'
        )


def load_country_data(iso3Code: str) -> Dict[str, Any]:
    """
    Load CIA World Factbook raw data by ISO3 code.

    Args:
        iso3Code: Three-letter ISO country code (e.g., 'USA', 'FRA', 'WLD')

    Returns:
        Dict containing the raw CIA data for the country

    Raises:
        ValueError: If ISO3 code is not found in the mapping
        FileNotFoundError: If the JSON file doesn't exist

    Examples:
        >>> data = load_country_data('USA')
        >>> data = load_country_data('WLD')
    """
    # Normalize to uppercase
    iso3Code = iso3Code.upper()

    # Look up the CIA code and region
    if iso3Code not in ISO3_TO_CIA:
        available = list(ISO3_TO_CIA.keys())[:10]
        raise ValueError(f"Unknown ISO3 code: {iso3Code}. Examples: {available}...")

    mapping = ISO3_TO_CIA[iso3Code]
    cia_code = mapping['cia_code']
    region_folder = mapping['region_folder']

    # Build the file path
    raw_data_folder = get_raw_data_folder()
    file_path = os.path.join(raw_data_folder, region_folder, f'{cia_code}.json')

    # Load and return the data
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_country_info(iso3Code: str) -> Optional[Dict[str, str]]:
    """
    Get country info (CIA code, region, name) by ISO3 code without loading data.

    Args:
        iso3Code: Three-letter ISO country code

    Returns:
        Dict with 'cia_code', 'region_folder', 'country_name', 'region_name' or None if not found
    """
    iso3Code = iso3Code.upper()
    return ISO3_TO_CIA.get(iso3Code)


def list_available_countries() -> list:
    """
    List all available ISO3 codes.

    Returns:
        List of ISO3 codes sorted alphabetically
    """
    return sorted(ISO3_TO_CIA.keys())


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    from pprint import pprint

    # Test the mapping
    print("=" * 60)
    print("ISO3 TO CIA CODE MAPPING TEST")
    print("=" * 60)

    test_codes = ['USA', 'FRA', 'WLD', 'DEU', 'CHN', 'KEN', 'BRA', 'JPN']

    for code in test_codes:
        info = get_country_info(code)
        if info:
            print(f"{code}: {info['country_name']} ({info['cia_code']}) - {info['region_folder']}")

    print(f"\nTotal available countries: {len(list_available_countries())}")

    # Test data loading
    print("\n" + "=" * 60)
    print("DATA LOADING TEST")
    print("=" * 60)

    for code in ['USA', 'WLD']:
        try:
            data = load_country_data(code)
            sections = list(data.keys())
            print(f"\n{code} loaded successfully. Sections: {sections[:5]}...")
        except Exception as e:
            print(f"\n{code}: ERROR - {e}")
