import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_life_expectancy_at_birth(life_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse life expectancy at birth data from CIA World Factbook format.

    Handles ALL format variations found across 233 countries:
    1. With year estimate: "82.6 years (2024 est.)"
    2. Without year: "79.8 years"
    3. Empty dict (some small territories)
    4. NA values

    Note: Uses 'total population' key instead of 'total'

    Args:
        life_data: Dictionary with 'total population', 'male', 'female' keys
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured life expectancy data:
        {
            "life_expectancy": {
                "total": {"value": 82.6, "timestamp": "2024", "is_estimate": True},
                "male": {"value": 79.8, "timestamp": None, "is_estimate": False},
                "female": {"value": 85.5, "timestamp": None, "is_estimate": False}
            },
            "life_expectancy_note": ""
        }
    """
    if return_original:
        return life_data

    result = {
        "life_expectancy": {
            "total": {"value": None, "timestamp": None, "is_estimate": False},
            "male": {"value": None, "timestamp": None, "is_estimate": False},
            "female": {"value": None, "timestamp": None, "is_estimate": False}
        },
        "life_expectancy_note": ""
    }

    if not life_data or not isinstance(life_data, dict):
        return result

    # Patterns for different formats:
    # 1. "82.6 years (2024 est.)" or "79.8 years"
    # 2. "(2017 est.) 77.9 years" - year before value
    # 3. Just numbers: "75.6" or "79.6"
    PATTERN1 = re.compile(r'([\d.]+)\s*years?\s*(?:\((\d{4})\s*(est\.?)?\))?')
    PATTERN2 = re.compile(r'\((\d{4})\s*est\.\)\s*([\d.]+)\s*years?')

    def parse_field(field_data: dict, return_original: bool = False)-> dict:
        """Parse a single field (total population, male, or female)."""
        if return_original:
            return field_data

        parsed = {"value": None, "timestamp": None, "is_estimate": False}

        if not isinstance(field_data, dict):
            return parsed

        text = field_data.get('text', '').strip()

        # Handle NA or empty
        if not text or text.upper() == 'NA':
            return parsed

        # Try pattern 1: value first
        match = PATTERN1.search(text)
        if match:
            parsed["value"] = float(match.group(1))
            if match.group(2):
                parsed["timestamp"] = match.group(2)
            if match.group(3):
                parsed["is_estimate"] = True
            return parsed

        # Try pattern 2: year first
        match = PATTERN2.search(text)
        if match:
            parsed["timestamp"] = match.group(1)
            parsed["value"] = float(match.group(2))
            parsed["is_estimate"] = True
            return parsed

        # Fallback: try to extract just a number (no warning - this is a valid format)
        num_match = re.search(r'([\d.]+)', text)
        if num_match:
            parsed["value"] = float(num_match.group(1))

        return parsed

    # Parse each field - note 'total population' instead of 'total'
    field_mapping = {
        'total population': 'total',
        'male': 'male',
        'female': 'female'
    }

    for src_field, dst_field in field_mapping.items():
        if src_field in life_data:
            result["life_expectancy"][dst_field] = parse_field(life_data[src_field])

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {
        "total population": {"text": "80.9 years (2024 est.)"},
        "male": {"text": "78.7 years"},
        "female": {"text": "83.1 years"}
    }
    print("Test 1 - Standard format:")
    print(parse_life_expectancy_at_birth(test1))
    print()

    # Test Case 2: Empty dict
    print("Test 2 - Empty input:")
    print(parse_life_expectancy_at_birth({}))
