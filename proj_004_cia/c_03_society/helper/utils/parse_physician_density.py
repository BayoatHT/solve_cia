import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_physician_density(doctor_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse physician density from CIA World Factbook format.

    Handles formats:
    1. Standard: "2.61 physicians/1,000 population (2018)"
    2. NA values

    Args:
        doctor_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured physician density data:
        {
            "physician_density": {
                "value": 2.61,
                "unit": "physicians/1,000 population",
                "timestamp": "2018",
                "is_estimate": False
            },
            "physician_density_note": ""
        }
    """
    if return_original:
        return doctor_data

    result = {
        "physician_density": {
            "value": None,
            "unit": "physicians/1,000 population",
            "timestamp": None,
            "is_estimate": False
        },
        "physician_density_note": ""
    }

    if not doctor_data or not isinstance(doctor_data, dict):
        return result

    text = doctor_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "2.61 physicians/1,000 population (2018)"
    PATTERN = re.compile(
        r'([\d.]+)\s*physicians?/1,000\s*population\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["physician_density"]["value"] = float(match.group(1))
        if match.group(2):
            result["physician_density"]["timestamp"] = match.group(2)
        if match.group(3):
            result["physician_density"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number
        num_match = re.search(r'([\d.]+)', text)
        if num_match:
            result["physician_density"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for physician density: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "2.61 physicians/1,000 population (2018)"}
    print("Test 1 - Standard format:")
    print(parse_physician_density(test1))
    print()

    # Test Case 2: High value
    test2 = {"text": "5.11 physicians/1,000 population (2020)"}
    print("Test 2 - High value:")
    print(parse_physician_density(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_physician_density(test3))
