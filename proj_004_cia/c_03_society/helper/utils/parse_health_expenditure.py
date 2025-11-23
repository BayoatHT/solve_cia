import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_health_expenditure(health_data: dict, iso3Code: str = None) -> dict:
    """
    Parse health expenditure data from CIA World Factbook format.

    Handles formats:
    1. Standard: "18.8% of GDP (2020)"
    2. NA values

    Args:
        health_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured health expenditure data:
        {
            "health_expenditure": {
                "value": 18.8,
                "unit": "% of GDP",
                "timestamp": "2020",
                "is_estimate": False
            },
            "health_expenditure_note": ""
        }
    """
    result = {
        "health_expenditure": {
            "value": None,
            "unit": "% of GDP",
            "timestamp": None,
            "is_estimate": False
        },
        "health_expenditure_note": ""
    }

    if not health_data or not isinstance(health_data, dict):
        return result

    text = health_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "18.8% of GDP (2020)" or "18.8% of GDP (2020 est.)"
    PATTERN = re.compile(
        r'([\d.]+)%\s*(?:of\s*GDP)?\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["health_expenditure"]["value"] = float(match.group(1))
        if match.group(2):
            result["health_expenditure"]["timestamp"] = match.group(2)
        if match.group(3):
            result["health_expenditure"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a percentage
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            result["health_expenditure"]["value"] = float(pct_match.group(1))
            logger.warning(f"Partial parse for health expenditure: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "18.8% of GDP (2020)"}
    print("Test 1 - Standard format:")
    print(parse_health_expenditure(test1))
    print()

    # Test Case 2: With estimate
    test2 = {"text": "7.5% of GDP (2021 est.)"}
    print("Test 2 - With estimate:")
    print(parse_health_expenditure(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_health_expenditure(test3))
