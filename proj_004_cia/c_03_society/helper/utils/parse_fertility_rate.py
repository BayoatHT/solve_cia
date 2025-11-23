import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_fertility_rate(fertility_data: dict, iso3Code: str = None) -> dict:
    """
    Parse total fertility rate data from CIA World Factbook format.

    Handles formats:
    1. Standard: "1.84 children born/woman (2024 est.)"
    2. NA values

    Args:
        fertility_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured fertility rate data:
        {
            "fertility_rate": {
                "value": 1.84,
                "unit": "children born/woman",
                "timestamp": "2024",
                "is_estimate": True
            },
            "fertility_rate_note": ""
        }
    """
    result = {
        "fertility_rate": {
            "value": None,
            "unit": "children born/woman",
            "timestamp": None,
            "is_estimate": False
        },
        "fertility_rate_note": ""
    }

    if not fertility_data or not isinstance(fertility_data, dict):
        return result

    text = fertility_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "1.84 children born/woman (2024 est.)"
    PATTERN = re.compile(
        r'([\d.]+)\s*children?\s*born/woman\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["fertility_rate"]["value"] = float(match.group(1))
        if match.group(2):
            result["fertility_rate"]["timestamp"] = match.group(2)
        if match.group(3):
            result["fertility_rate"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number
        num_match = re.search(r'([\d.]+)', text)
        if num_match:
            result["fertility_rate"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for fertility rate: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "1.84 children born/woman (2024 est.)"}
    print("Test 1 - Standard format:")
    print(parse_fertility_rate(test1))
    print()

    # Test Case 2: NA
    test2 = {"text": "NA"}
    print("Test 2 - NA:")
    print(parse_fertility_rate(test2))
    print()

    # Test Case 3: Empty
    print("Test 3 - Empty:")
    print(parse_fertility_rate({}))
