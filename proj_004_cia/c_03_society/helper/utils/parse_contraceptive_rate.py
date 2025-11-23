import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_contraceptive_rate(contraceptive_data: dict, iso3Code: str = None) -> dict:
    """
    Parse contraceptive prevalence rate from CIA World Factbook format.

    Handles formats:
    1. Standard: "73.9% (2017/19)"
    2. With estimate: "65.5% (2019 est.)"
    3. NA values

    Args:
        contraceptive_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured contraceptive rate data
    """
    result = {
        "contraceptive_rate": {
            "value": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "contraceptive_rate_note": ""
    }

    if not contraceptive_data or not isinstance(contraceptive_data, dict):
        return result

    text = contraceptive_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "73.9% (2017/19)" or "65.5% (2019 est.)"
    PATTERN = re.compile(
        r'([\d.]+)%\s*(?:\(([^)]+)\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["contraceptive_rate"]["value"] = float(match.group(1))
        if match.group(2):
            year_info = match.group(2).strip()
            # Extract year or year range
            year_match = re.search(r'(\d{4}(?:/\d{2,4})?)', year_info)
            if year_match:
                result["contraceptive_rate"]["timestamp"] = year_match.group(1)
            if 'est' in year_info.lower():
                result["contraceptive_rate"]["is_estimate"] = True

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Year range
    test1 = {"text": "73.9% (2017/19)"}
    print("Test 1 - Year range:")
    print(parse_contraceptive_rate(test1))
    print()

    # Test Case 2: With estimate
    test2 = {"text": "65.5% (2019 est.)"}
    print("Test 2 - With estimate:")
    print(parse_contraceptive_rate(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_contraceptive_rate(test3))
