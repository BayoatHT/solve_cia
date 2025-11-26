import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_air_pollutants(pollutants_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse air pollutants from CIA Environment section for a given country.

    Args:
        pollutants_data: The 'Air pollutants' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured air pollutants data
    """
    result = {
        "air_pollutants": {
            "particulate_matter": None,
            "particulate_matter_unit": "micrograms per cubic meter",
            "carbon_dioxide_emissions": None,
            "carbon_dioxide_unit": "megatons",
            "methane_emissions": None,
            "methane_unit": "megatons",
            "timestamp": None,
            "is_estimate": False
        },
        "air_pollutants_note": ""
    }

    if return_original:
        return pollutants_data

    if not pollutants_data or not isinstance(pollutants_data, dict):
        return result

    def extract_value_and_year(text):
        """Extract numeric value and year from text like '7.18 micrograms per cubic meter (2019 est.)'"""
        if not text:
            return None, None, False

        value = None
        year = None
        is_est = False

        # Extract number
        num_match = re.search(r'([\d,]+\.?\d*)', text)
        if num_match:
            value = float(num_match.group(1).replace(',', ''))

        # Extract year
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            year = year_match.group(1)
            is_est = 'est' in text.lower()

        return value, year, is_est

    # Parse particulate matter
    pm_data = pollutants_data.get('particulate matter emissions', {})
    if pm_data and isinstance(pm_data, dict):
        text = pm_data.get('text', '')
        if text and text.upper() != 'NA':
            value, year, is_est = extract_value_and_year(text)
            result['air_pollutants']['particulate_matter'] = value
            if year:
                result['air_pollutants']['timestamp'] = year
            result['air_pollutants']['is_estimate'] = is_est

    # Parse CO2 emissions
    co2_data = pollutants_data.get('carbon dioxide emissions', {})
    if co2_data and isinstance(co2_data, dict):
        text = co2_data.get('text', '')
        if text and text.upper() != 'NA':
            value, year, is_est = extract_value_and_year(text)
            result['air_pollutants']['carbon_dioxide_emissions'] = value
            if year and not result['air_pollutants']['timestamp']:
                result['air_pollutants']['timestamp'] = year

    # Parse methane emissions
    methane_data = pollutants_data.get('methane emissions', {})
    if methane_data and isinstance(methane_data, dict):
        text = methane_data.get('text', '')
        if text and text.upper() != 'NA':
            value, year, is_est = extract_value_and_year(text)
            result['air_pollutants']['methane_emissions'] = value
            if year and not result['air_pollutants']['timestamp']:
                result['air_pollutants']['timestamp'] = year

    # Check for note
    note = pollutants_data.get('note', '')
    if note:
        result['air_pollutants_note'] = clean_text(note)

    return result


if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_air_pollutants")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'DEU']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            pollutants_data = raw_data.get('Environment', {}).get('Air pollutants', {})
            result = parse_air_pollutants(pollutants_data, iso3)
            if result and result['air_pollutants']['particulate_matter']:
                ap = result['air_pollutants']
                print(f"  PM: {ap['particulate_matter']} {ap['particulate_matter_unit']}")
                print(f"  CO2: {ap['carbon_dioxide_emissions']} {ap['carbon_dioxide_unit']}")
                print(f"  Methane: {ap['methane_emissions']} {ap['methane_unit']}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
