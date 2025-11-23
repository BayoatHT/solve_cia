import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_infant_mortality(infant_data: dict, iso3Code: str = None) -> dict:
    """
    Parse infant mortality rate data from CIA World Factbook format.

    Handles ALL format variations found across 233 countries:
    1. With year estimate: "5.1 deaths/1,000 live births (2024 est.)"
    2. Without year: "5.4 deaths/1,000 live births"
    3. Empty dict (some small territories)
    4. NA values

    Args:
        infant_data: Dictionary with 'total', 'male', 'female' keys
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured infant mortality data:
        {
            "infant_mortality": {
                "total": {"value": 5.1, "timestamp": "2024", "is_estimate": True},
                "male": {"value": 5.4, "timestamp": None, "is_estimate": False},
                "female": {"value": 4.7, "timestamp": None, "is_estimate": False},
                "unit": "deaths/1,000 live births"
            },
            "infant_mortality_note": ""
        }
    """
    result = {
        "infant_mortality": {
            "total": {"value": None, "timestamp": None, "is_estimate": False},
            "male": {"value": None, "timestamp": None, "is_estimate": False},
            "female": {"value": None, "timestamp": None, "is_estimate": False},
            "unit": "deaths/1,000 live births"
        },
        "infant_mortality_note": ""
    }

    if not infant_data or not isinstance(infant_data, dict):
        return result

    # Pattern: "5.1 deaths/1,000 live births (2024 est.)"
    PATTERN = re.compile(
        r'([\d.]+)\s*deaths?/1,000\s*live\s*births?\s*(?:\((\d{4})\s*(est\.?)?\))?'
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
                logger.warning(f"Partial parse for infant mortality: {text[:50]}...")

        return parsed

    # Parse each field
    for field in ['total', 'male', 'female']:
        if field in infant_data:
            result["infant_mortality"][field] = parse_field(infant_data[field])

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {
        "total": {"text": "5.1 deaths/1,000 live births (2024 est.)"},
        "male": {"text": "5.4 deaths/1,000 live births"},
        "female": {"text": "4.7 deaths/1,000 live births"}
    }
    print("Test 1 - Standard format:")
    print(parse_infant_mortality(test1))
    print()

    # Test Case 2: Empty dict
    print("Test 2 - Empty input:")
    print(parse_infant_mortality({}))
