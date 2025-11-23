import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_median_age(median_data: dict, iso3Code: str = None) -> dict:
    """
    Parse median age data from CIA World Factbook format.

    Handles ALL format variations found across 233 countries:
    1. With year estimate: "38.3 years (2024 est.)"
    2. Without year: "35.9 years"
    3. Empty dict for male/female (some countries)
    4. NA values

    Args:
        median_data: Dictionary with 'total', 'male', 'female' keys
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured median age data:
        {
            "median_age": {
                "total": {"value": 38.3, "timestamp": "2024", "is_estimate": True},
                "male": {"value": 35.9, "timestamp": None, "is_estimate": False},
                "female": {"value": 40.1, "timestamp": None, "is_estimate": False}
            },
            "median_age_note": ""
        }
    """
    result = {
        "median_age": {
            "total": {"value": None, "timestamp": None, "is_estimate": False},
            "male": {"value": None, "timestamp": None, "is_estimate": False},
            "female": {"value": None, "timestamp": None, "is_estimate": False}
        },
        "median_age_note": ""
    }

    if not median_data or not isinstance(median_data, dict):
        return result

    # Regex pattern for parsing: "38.3 years (2024 est.)" or "35.9 years"
    # Pattern handles: number, optional decimal, "years", optional (year est.)
    PATTERN = re.compile(
        r'([\d.]+)\s*years?\s*(?:\((\d{4})\s*(est\.?)?\))?'
    )

    def parse_field(field_data: dict) -> dict:
        """Parse a single field (total, male, or female)."""
        parsed = {"value": None, "timestamp": None, "is_estimate": False}

        if not isinstance(field_data, dict):
            return parsed

        text = field_data.get('text', '').strip()

        # Handle NA or empty
        if not text or text.upper() == 'NA':
            return parsed

        match = PATTERN.search(text)
        if match:
            parsed["value"] = float(match.group(1))
            if match.group(2):
                parsed["timestamp"] = match.group(2)
            if match.group(3):
                parsed["is_estimate"] = True
        else:
            # Fallback: try to extract just a number
            num_match = re.search(r'([\d.]+)', text)
            if num_match:
                parsed["value"] = float(num_match.group(1))
                logger.warning(f"Partial parse for median age: {text[:50]}...")

        return parsed

    # Parse each field
    for field in ['total', 'male', 'female']:
        if field in median_data:
            result["median_age"][field] = parse_field(median_data[field])

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {
        "total": {"text": "38.9 years (2022 est.)"},
        "male": {"text": "37.8 years"},
        "female": {"text": "40 years"}
    }
    print("Test 1 - Standard format:")
    print(parse_median_age(test1))
    print()

    # Test Case 2: Empty male/female (Cook Islands format)
    test2 = {
        "total": {"text": "40 years (2021 est.)"},
        "male": {},
        "female": {}
    }
    print("Test 2 - Empty male/female:")
    print(parse_median_age(test2))
    print()

    # Test Case 3: Empty input
    print("Test 3 - Empty input:")
    print(parse_median_age({}))
