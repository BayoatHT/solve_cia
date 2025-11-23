import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_reproduction_rate(reproduction_data: dict, iso3Code: str = None) -> dict:
    """
    Parse net reproduction rate from CIA World Factbook format.

    Handles formats:
    1. Standard: "0.9 (2024 est.)"
    2. NA values

    Args:
        reproduction_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured reproduction rate data
    """
    result = {
        "reproduction_rate": {
            "value": None,
            "timestamp": None,
            "is_estimate": False
        },
        "reproduction_rate_note": ""
    }

    if not reproduction_data or not isinstance(reproduction_data, dict):
        return result

    text = reproduction_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "0.9 (2024 est.)"
    PATTERN = re.compile(
        r'([\d.]+)\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["reproduction_rate"]["value"] = float(match.group(1))
        if match.group(2):
            result["reproduction_rate"]["timestamp"] = match.group(2)
        if match.group(3):
            result["reproduction_rate"]["is_estimate"] = True

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "0.9 (2024 est.)"}
    print("Test 1 - Standard format:")
    print(parse_reproduction_rate(test1))
    print()

    # Test Case 2: NA
    test2 = {"text": "NA"}
    print("Test 2 - NA:")
    print(parse_reproduction_rate(test2))
