import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_death_rate(death_rate_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse death rate data from CIA World Factbook format.

    Handles ALL format variations found across 234 countries:
    1. Standard: "8.5 deaths/1,000 population (2024 est.)"
    2. NA values

    Args:
        death_rate_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured death rate data:
        {
            "death_rate": {
                "value": 8.5,
                "unit": "deaths/1,000 population",
                "timestamp": "2024",
                "is_estimate": True
            },
            "death_rate_note": ""
        }
    """
    if return_original:
        return death_rate_data

    result = {
        "death_rate": {
            "value": None,
            "unit": "deaths/1,000 population",
            "timestamp": None,
            "is_estimate": False
        },
        "death_rate_note": ""
    }

    if not death_rate_data or not isinstance(death_rate_data, dict):
        return result

    text = death_rate_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "8.5 deaths/1,000 population (2024 est.)"
    PATTERN = re.compile(
        r'([\d.]+)\s*deaths?/1,000\s*population\s*(?:\((\d{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["death_rate"]["value"] = float(match.group(1))
        if match.group(2):
            result["death_rate"]["timestamp"] = match.group(2)
        if match.group(3):
            result["death_rate"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number
        num_match = re.search(r'([\d.]+)', text)
        if num_match:
            result["death_rate"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for death rate: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "8.5 deaths/1,000 population (2024 est.)"}
    print("Test 1 - Standard format:")
    print(parse_death_rate(test1))
    print()

    # Test Case 2: NA
    test2 = {"text": "NA"}
    print("Test 2 - NA:")
    print(parse_death_rate(test2))
    print()

    # Test Case 3: Empty
    print("Test 3 - Empty:")
    print(parse_death_rate({}))
