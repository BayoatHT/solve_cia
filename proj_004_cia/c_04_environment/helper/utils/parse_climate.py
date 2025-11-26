import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_climate(climate_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse climate from CIA Environment section for a given country.

    Args:
        climate_data: The 'Climate' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured climate data
    """
    result = {
        "climate": {
            "description": None,
            "note": None
        },
        "climate_extremes": {
            "coldest_places": None,
            "hottest_places": None,
            "driest_places": None,
            "wettest_places": None
        },
        "climate_note": ""
    }

    if return_original:
        return climate_data

    if not climate_data or not isinstance(climate_data, dict):
        return result

    # Extract main description
    text = climate_data.get('text', '')
    if text and text.upper() != 'NA':
        result['climate']['description'] = clean_text(text)

    # Extract note
    note = climate_data.get('note', '')
    if note:
        result['climate']['note'] = clean_text(note)

    # Handle world data with extreme locations
    for key in climate_data:
        if 'coldest' in key.lower():
            data = climate_data.get(key, {})
            result['climate_extremes']['coldest_places'] = clean_text(data.get('text', '')) if isinstance(data, dict) else None
        elif 'hottest' in key.lower():
            data = climate_data.get(key, {})
            result['climate_extremes']['hottest_places'] = clean_text(data.get('text', '')) if isinstance(data, dict) else None
        elif 'driest' in key.lower():
            data = climate_data.get(key, {})
            result['climate_extremes']['driest_places'] = clean_text(data.get('text', '')) if isinstance(data, dict) else None
        elif 'wettest' in key.lower():
            data = climate_data.get(key, {})
            result['climate_extremes']['wettest_places'] = clean_text(data.get('text', '')) if isinstance(data, dict) else None

    return result


if __name__ == "__main__":
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_climate")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'WLD']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            climate_data = raw_data.get('Environment', {}).get('Climate', {})
            result = parse_climate(climate_data, iso3)
            if result and result['climate']['description']:
                desc = result['climate']['description']
                print(f"  {desc[:80]}...")
                extremes = result['climate_extremes']
                if any(extremes.values()):
                    print(f"  Has extremes data")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
