import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_urbanization(urb_data: dict, iso3Code: str = None) -> dict:
    """
    Parse urbanization data from CIA World Factbook format.

    Handles nested structure:
    {
        "urban population": {"text": "83.3% of total population (2023)"},
        "rate of urbanization": {"text": "0.96% annual rate of change (2020-25 est.)"}
    }

    Args:
        urb_data: Dictionary with nested structure
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured urbanization data
    """
    result = {
        "urbanization": {
            "urban_population_percent": None,
            "urban_population_year": None,
            "rate_of_urbanization": None,
            "rate_period": None,
            "is_estimate": False
        },
        "urbanization_note": ""
    }

    if not urb_data or not isinstance(urb_data, dict):
        return result

    # Extract urban population percentage
    if 'urban population' in urb_data:
        urban_data = urb_data['urban population']
        text = urban_data.get('text', '') if isinstance(urban_data, dict) else str(urban_data)

        if text and text.upper() != 'NA':
            # Pattern: "83.3% of total population (2023)"
            pct_match = re.search(r'([\d.]+)%', text)
            year_match = re.search(r'\((\d{4})\)', text)

            if pct_match:
                result["urbanization"]["urban_population_percent"] = float(pct_match.group(1))
            if year_match:
                result["urbanization"]["urban_population_year"] = year_match.group(1)

    # Extract rate of urbanization
    if 'rate of urbanization' in urb_data:
        rate_data = urb_data['rate of urbanization']
        text = rate_data.get('text', '') if isinstance(rate_data, dict) else str(rate_data)

        if text and text.upper() != 'NA':
            # Pattern: "0.96% annual rate of change (2020-25 est.)"
            rate_match = re.search(r'(-?[\d.]+)%', text)
            period_match = re.search(r'\((\d{4}-\d{2,4})\s*(est\.?)?\)', text)

            if rate_match:
                result["urbanization"]["rate_of_urbanization"] = float(rate_match.group(1))
            if period_match:
                result["urbanization"]["rate_period"] = period_match.group(1)
                if period_match.group(2):
                    result["urbanization"]["is_estimate"] = True

    # Extract note
    if 'note' in urb_data:
        note = urb_data['note']
        if isinstance(note, str):
            note = re.sub(r'<[^>]+>', '', note).strip()
            note = re.sub(r'^note\s*\d*:\s*', '', note, flags=re.IGNORECASE)
            result["urbanization_note"] = note

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {
        "urban population": {"text": "83.3% of total population (2023)"},
        "rate of urbanization": {"text": "0.96% annual rate of change (2020-25 est.)"}
    }
    print("Test 1 - Standard format:")
    print(parse_urbanization(test1))
    print()

    # Test Case 2: Negative rate
    test2 = {
        "urban population": {"text": "60.7% of total population (2023)"},
        "rate of urbanization": {"text": "-0.35% annual rate of change (2020-25 est.)"}
    }
    print("Test 2 - Negative rate:")
    print(parse_urbanization(test2))
