import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_air_pollutants(pollutants_data: dict, iso3Code: str = None) -> dict:
    """
    Parse air pollutants data from CIA World Factbook format.

    Args:
        pollutants_data: Dictionary with air pollutants information
        iso3Code: Optional ISO3 country code for logging

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
    test_data = {
        "particulate matter emissions": {"text": "7.18 micrograms per cubic meter (2019 est.)"},
        "carbon dioxide emissions": {"text": "5,006.3 megatons (2016 est.)"},
        "methane emissions": {"text": "685.74 megatons (2020 est.)"}
    }
    print(parse_air_pollutants(test_data))
