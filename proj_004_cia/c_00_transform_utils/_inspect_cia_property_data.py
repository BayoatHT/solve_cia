#!/usr/bin/env python3
"""
CIA Data Inspector Function
==========================

Function to extract and inspect specific property data from CIA JSON files.
Always includes World data first, then specified countries.
Supports multi-level nested data extraction.

Author: CIA Data Parsing Project  
Date: 2025-07-08
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional

# Import required modules (adjust paths as needed)
from impact_titan.impact_3_data.c_sources.c_file_sources.json_imports.a_usa_cia._basic_helpers.a_files.function_generated.cia_code_names import cia_code_names
from impact_titan.impact_3_data.c_sources.c_file_sources.json_imports.a_usa_cia._basic_helpers.a_files.cia_region_names import cia_region_names
from proj_004_cia.__logger.logger import app_logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def inspect_cia_property_data(
    section_key: str,
    property_key: str,
    countries: Optional[List[str]] = None,
    sub_property_key: Optional[str] = None,
    sub_sub_property_key: Optional[str] = None,
    limit_countries: int = 10
) -> List[Dict[str, Any]]:
    """
    Extract and inspect specific property data from CIA JSON files.
    Always includes World data first, then specified countries.

    Args:
        section_key: Main section (e.g., 'Government', 'Geography')
        property_key: Property within section (e.g., 'Legal system', 'Country name')
        countries: List of ISO3 codes to inspect (e.g., ['USA', 'ESP', 'FRA'])
        sub_property_key: Optional sub-property (e.g., 'conventional short form')
        sub_sub_property_key: Optional sub-sub-property (e.g., 'text')
        limit_countries: Maximum number of countries to include (for performance)

    Returns:
        List of dictionaries with format [{iso3Code: extracted_data}, ...]
        First item is always World data (WLD), followed by country data

    Examples:
        # Simple property extraction
        inspect_cia_property_data('Government', 'Legal system', ['USA', 'FRA'])

        # Nested property extraction  
        inspect_cia_property_data('Government', 'Country name', ['USA'], 'conventional short form', 'text')

        # Multiple countries
        inspect_cia_property_data('Government', 'Government type', ['USA', 'ESP', 'FRA', 'DEU', 'JPN'])
    """

    if app_logger:
        app_logger.info(
            f"🔍 Inspecting CIA property: {section_key}.{property_key}")

    # Setup directories
    all_jsons_folder = 'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia/_raw_data'

    # Initialize result array
    inspection_results = []

    # Step 1: Always get World data first (WLD)
    world_data = _extract_property_for_country('WLD', section_key, property_key,
                                               sub_property_key, sub_sub_property_key, all_jsons_folder)
    if world_data is not None:
        inspection_results.append({'WLD': world_data})
        if app_logger:
            app_logger.success(
                f"✅ World data extracted for {section_key}.{property_key}")
    else:
        inspection_results.append({'WLD': 'NO_DATA_FOUND'})
        if app_logger:
            app_logger.warning(
                f"⚠️ No World data found for {section_key}.{property_key}")

    # Step 2: Process specified countries or get samples
    target_countries = countries if countries else _get_sample_countries(
        limit_countries)

    # Limit countries for performance
    if len(target_countries) > limit_countries:
        target_countries = target_countries[:limit_countries]
        if app_logger:
            app_logger.info(
                f"Limited to {limit_countries} countries for performance")

    # Extract data for each country
    for iso3_code in target_countries:
        try:
            country_data = _extract_property_for_country(iso3_code, section_key, property_key,
                                                         sub_property_key, sub_sub_property_key, all_jsons_folder)

            if country_data is not None:
                inspection_results.append({iso3_code: country_data})
                if app_logger:
                    app_logger.success(f"✅ {iso3_code}: Data extracted")
            else:
                inspection_results.append({iso3_code: 'NO_DATA_FOUND'})
                if app_logger:
                    app_logger.warning(f"⚠️ {iso3_code}: No data found")

        except Exception as e:
            inspection_results.append({iso3_code: f'ERROR: {str(e)}'})
            if app_logger:
                app_logger.error(f"❌ {iso3_code}: Error extracting data - {e}")

    # Summary
    successful_extractions = len(
        [r for r in inspection_results if not isinstance(list(r.values())[0], str)])
    total_attempted = len(inspection_results)

    if app_logger:
        app_logger.business(f"📊 Inspection complete: {successful_extractions}/{total_attempted} successful extractions",
                            division="data_inspection", function="property_extraction")

    return inspection_results


def _extract_property_for_country(
    iso3_code: str,
    section_key: str,
    property_key: str,
    sub_property_key: Optional[str],
    sub_sub_property_key: Optional[str],
    all_jsons_folder: str
) -> Any:
    """
    Extract property data for a specific country from its JSON file.

    Args:
        iso3_code: ISO3 country code (e.g., 'USA', 'WLD')
        section_key: Main section name
        property_key: Property name within section
        sub_property_key: Optional sub-property
        sub_sub_property_key: Optional sub-sub-property
        all_jsons_folder: Base folder containing JSON files

    Returns:
        Extracted data or None if not found
    """

    # Find the JSON file for this country
    json_file_path = _find_json_file_for_country(iso3_code, all_jsons_folder)

    if not json_file_path:
        logger.warning(f"JSON file not found for {iso3_code}")
        return None

    # Load the JSON data
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            country_info = json.load(file)
    except Exception as e:
        logger.error(f"Error loading JSON for {iso3_code}: {e}")
        return None

    # Navigate through the nested structure
    data = country_info

    # Level 1: Section (e.g., 'Government')
    if section_key in data:
        data = data[section_key]
    else:
        logger.debug(f"Section '{section_key}' not found in {iso3_code}")
        return None

    # Level 2: Property (e.g., 'Legal system')
    if property_key in data:
        data = data[property_key]
    else:
        logger.debug(
            f"Property '{property_key}' not found in {iso3_code}.{section_key}")
        return None

    # Level 3: Sub-property (optional, e.g., 'conventional short form')
    if sub_property_key:
        if isinstance(data, dict) and sub_property_key in data:
            data = data[sub_property_key]
        else:
            logger.debug(
                f"Sub-property '{sub_property_key}' not found in {iso3_code}.{section_key}.{property_key}")
            return None

    # Level 4: Sub-sub-property (optional, e.g., 'text')
    if sub_sub_property_key:
        if isinstance(data, dict) and sub_sub_property_key in data:
            data = data[sub_sub_property_key]
        else:
            logger.debug(
                f"Sub-sub-property '{sub_sub_property_key}' not found")
            return None

    return data


def _find_json_file_for_country(iso3_code: str, all_jsons_folder: str) -> Optional[str]:
    """
    Find the JSON file path for a given ISO3 code.

    Args:
        iso3_code: ISO3 country code
        all_jsons_folder: Base folder containing regional subdirectories

    Returns:
        Full path to JSON file or None if not found
    """

    # Special handling for World data
    if iso3_code == 'WLD':
        world_file = os.path.join(all_jsons_folder, 'world', 'xx.json')
        if os.path.exists(world_file):
            return world_file
        else:
            logger.warning("World data file (world/xx.json) not found")
            return None

    # Find the CIA code for this ISO3 code
    cia_code = None
    region_folder = None

    for code, country_info in cia_code_names.items():
        if country_info.get('iso3Code') == iso3_code:
            cia_code = code
            region_name = country_info.get('region_name', '')

            # Find the region folder name
            for folder_name, display_name in cia_region_names.items():
                if display_name.lower() == region_name.lower():
                    region_folder = folder_name
                    break
            break

    if not cia_code or not region_folder:
        logger.warning(f"CIA code or region not found for {iso3_code}")
        return None

    # Construct the file path
    json_file_path = os.path.join(
        all_jsons_folder, region_folder, f'{cia_code}.json')

    if os.path.exists(json_file_path):
        return json_file_path
    else:
        logger.warning(f"JSON file not found: {json_file_path}")
        return None


def _get_sample_countries(limit: int = 10) -> List[str]:
    """
    Get a diverse sample of countries for testing.

    Args:
        limit: Maximum number of countries to return

    Returns:
        List of ISO3 codes representing diverse countries
    """

    # Get a diverse sample from different regions
    sample_countries = []

    # Add major countries from different regions
    priority_countries = ['USA', 'CHN', 'DEU', 'JPN',
                          'GBR', 'FRA', 'BRA', 'IND', 'RUS', 'AUS']

    # Add from the priority list first
    for country in priority_countries:
        if len(sample_countries) < limit:
            sample_countries.append(country)

    # If we need more, add additional countries
    if len(sample_countries) < limit:
        all_iso3_codes = [info.get('iso3Code') for info in cia_code_names.values()
                          if info.get('iso3Code') and info.get('iso3Code') not in sample_countries]

        additional_needed = limit - len(sample_countries)
        sample_countries.extend(all_iso3_codes[:additional_needed])

    return sample_countries


# Test and example usage
if __name__ == "__main__":
    print("="*80)
    print("CIA DATA INSPECTOR - TEST RUNS")
    print("="*80)

    # Test 1: Simple property extraction (Legal system)
    print("\n1. Testing Legal System extraction:")
    legal_system_data = inspect_cia_property_data(
        section_key='Government',
        property_key='Legal system',
        countries=['USA', 'FRA', 'DEU'],
        limit_countries=5
    )

    for item in legal_system_data:
        for iso3_code, data in item.items():
            print(
                f"  {iso3_code}: {str(data)[:100]}{'...' if len(str(data)) > 100 else ''}")

    # Test 2: Nested property extraction (Country name)
    print("\n2. Testing Country Name extraction (nested):")
    country_name_data = inspect_cia_property_data(
        section_key='Government',
        property_key='Country name',
        countries=['USA', 'ESP'],
        sub_property_key='conventional short form',
        sub_sub_property_key='text',
        limit_countries=3
    )

    for item in country_name_data:
        for iso3_code, data in item.items():
            print(f"  {iso3_code}: {data}")

    # Test 3: Government type
    print("\n3. Testing Government Type extraction:")
    gov_type_data = inspect_cia_property_data(
        section_key='Government',
        property_key='Government type',
        countries=['USA', 'FRA', 'CHN', 'JPN'],
        limit_countries=6
    )

    for item in gov_type_data:
        for iso3_code, data in item.items():
            print(
                f"  {iso3_code}: {str(data)[:80]}{'...' if len(str(data)) > 80 else ''}")

    print("\n" + "="*80)
    print("✅ CIA DATA INSPECTOR READY FOR USE")
    print("✅ Always includes World data first")
    print("✅ Supports multi-level property extraction")
    print("✅ Perfect for testing parser functions")
    print("="*80)
