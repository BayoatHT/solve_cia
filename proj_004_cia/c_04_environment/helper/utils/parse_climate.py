import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_climate(climate_data: dict, iso3Code: str = None) -> dict:
    """
    Parse climate data from CIA World Factbook format.

    Args:
        climate_data: Dictionary with climate information
        iso3Code: Optional ISO3 country code for logging

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
    test_data = {
        "text": "mostly temperate, but tropical in Hawaii",
        "note": "<strong>note:</strong> Denali is the coldest mountain"
    }
    print(parse_climate(test_data))
