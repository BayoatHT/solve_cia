import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_education_expenditure(education_data: dict, iso3Code: str = None) -> dict:
    """
    Parse education expenditure data from CIA World Factbook format.

    Handles formats:
    1. Standard: "6.1% of GDP (2020 est.)"
    2. NA values

    Args:
        education_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured education expenditure data:
        {
            "education_expenditure": {
                "value": 6.1,
                "unit": "% of GDP",
                "timestamp": "2020",
                "is_estimate": True
            },
            "education_expenditure_note": ""
        }
    """
    result = {
        "education_expenditure": {
            "value": None,
            "unit": "% of GDP",
            "timestamp": None,
            "is_estimate": False
        },
        "education_expenditure_note": ""
    }

    if not education_data or not isinstance(education_data, dict):
        return result

    text = education_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "6.1% of GDP (2020 est.)"
    PATTERN = re.compile(
        r'([\d.]+)%\s*of\s*GDP\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["education_expenditure"]["value"] = float(match.group(1))
        if match.group(2):
            result["education_expenditure"]["timestamp"] = match.group(2)
        if match.group(3):
            result["education_expenditure"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a percentage
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            result["education_expenditure"]["value"] = float(pct_match.group(1))
            logger.warning(f"Partial parse for education expenditure: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "6.1% of GDP (2020 est.)"}
    print("Test 1 - Standard format:")
    print(parse_education_expenditure(test1))
    print()

    # Test Case 2: Without estimate
    test2 = {"text": "3.6% of GDP (2021)"}
    print("Test 2 - Without estimate:")
    print(parse_education_expenditure(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_education_expenditure(test3))
