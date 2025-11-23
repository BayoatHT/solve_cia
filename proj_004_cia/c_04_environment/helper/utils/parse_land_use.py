import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_land_use(land_data: dict, iso3Code: str = None) -> dict:
    """
    Parse land use data from CIA World Factbook format.

    Args:
        land_data: Dictionary with land use information
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured land use data
    """
    result = {
        "land_use": {
            "agricultural_land": None,
            "arable_land": None,
            "permanent_crops": None,
            "permanent_pasture": None,
            "forest": None,
            "other": None,
            "timestamp": None,
            "is_estimate": False
        },
        "land_use_note": ""
    }

    if not land_data or not isinstance(land_data, dict):
        return result

    def extract_percentage_and_year(text):
        """Extract percentage and year from text like '44.5% (2018 est.)'"""
        if not text:
            return None, None, False

        pct = None
        year = None
        is_est = False

        # Extract percentage
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            pct = float(pct_match.group(1))

        # Extract year
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            year = year_match.group(1)
            is_est = 'est' in text.lower()

        return pct, year, is_est

    # Parse agricultural land total
    ag_data = land_data.get('agricultural land', {})
    if ag_data and isinstance(ag_data, dict):
        text = ag_data.get('text', '')
        if text and text.upper() != 'NA':
            pct, year, is_est = extract_percentage_and_year(text)
            result['land_use']['agricultural_land'] = pct
            result['land_use']['timestamp'] = year
            result['land_use']['is_estimate'] = is_est

    # Parse arable land
    arable_data = land_data.get('agricultural land: arable land', {})
    if arable_data and isinstance(arable_data, dict):
        text = arable_data.get('text', '')
        if text and text.upper() != 'NA':
            pct, _, _ = extract_percentage_and_year(text)
            result['land_use']['arable_land'] = pct

    # Parse permanent crops
    crops_data = land_data.get('agricultural land: permanent crops', {})
    if crops_data and isinstance(crops_data, dict):
        text = crops_data.get('text', '')
        if text and text.upper() != 'NA':
            pct, _, _ = extract_percentage_and_year(text)
            result['land_use']['permanent_crops'] = pct

    # Parse permanent pasture
    pasture_data = land_data.get('agricultural land: permanent pasture', {})
    if pasture_data and isinstance(pasture_data, dict):
        text = pasture_data.get('text', '')
        if text and text.upper() != 'NA':
            pct, _, _ = extract_percentage_and_year(text)
            result['land_use']['permanent_pasture'] = pct

    # Parse forest
    forest_data = land_data.get('forest', {})
    if forest_data and isinstance(forest_data, dict):
        text = forest_data.get('text', '')
        if text and text.upper() != 'NA':
            pct, _, _ = extract_percentage_and_year(text)
            result['land_use']['forest'] = pct

    # Parse other
    other_data = land_data.get('other', {})
    if other_data and isinstance(other_data, dict):
        text = other_data.get('text', '')
        if text and text.upper() != 'NA':
            pct, _, _ = extract_percentage_and_year(text)
            result['land_use']['other'] = pct

    # Check for note
    note = land_data.get('note', '')
    if note:
        result['land_use_note'] = clean_text(note) if isinstance(note, str) else clean_text(note.get('text', ''))

    return result


if __name__ == "__main__":
    test_data = {
        "agricultural land": {"text": "44.5% (2018 est.)"},
        "agricultural land: arable land": {"text": "arable land: 16.8% (2018 est.)"},
        "forest": {"text": "33.3% (2018 est.)"}
    }
    print(parse_land_use(test_data))
