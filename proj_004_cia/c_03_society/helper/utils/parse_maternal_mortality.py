import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_maternal_mortality(maternity_data: dict, iso3Code: str = None) -> dict:
    """
    Parse maternal mortality ratio from CIA World Factbook format.

    Handles formats:
    1. Standard: "21 deaths/100,000 live births (2020 est.)"
    2. NA values

    Args:
        maternity_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured maternal mortality data:
        {
            "maternal_mortality_ratio": {
                "value": 21,
                "unit": "deaths/100,000 live births",
                "timestamp": "2020",
                "is_estimate": True
            },
            "maternal_mortality_ratio_note": ""
        }
    """
    result = {
        "maternal_mortality_ratio": {
            "value": None,
            "unit": "deaths/100,000 live births",
            "timestamp": None,
            "is_estimate": False
        },
        "maternal_mortality_ratio_note": ""
    }

    if not maternity_data or not isinstance(maternity_data, dict):
        return result

    text = maternity_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "21 deaths/100,000 live births (2020 est.)"
    PATTERN = re.compile(
        r'([\d,]+)\s*deaths?/100,000\s*live\s*births?\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        # Remove commas from number
        value_str = match.group(1).replace(',', '')
        result["maternal_mortality_ratio"]["value"] = int(value_str)
        if match.group(2):
            result["maternal_mortality_ratio"]["timestamp"] = match.group(2)
        if match.group(3):
            result["maternal_mortality_ratio"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number
        num_match = re.search(r'([\d,]+)', text)
        if num_match:
            value_str = num_match.group(1).replace(',', '')
            result["maternal_mortality_ratio"]["value"] = int(value_str)
            logger.warning(f"Partial parse for maternal mortality: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "21 deaths/100,000 live births (2020 est.)"}
    print("Test 1 - Standard format:")
    print(parse_maternal_mortality(test1))
    print()

    # Test Case 2: Higher value
    test2 = {"text": "1,150 deaths/100,000 live births (2020 est.)"}
    print("Test 2 - High value with comma:")
    print(parse_maternal_mortality(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_maternal_mortality(test3))
