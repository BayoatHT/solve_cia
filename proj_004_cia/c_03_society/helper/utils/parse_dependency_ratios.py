import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_dependency_ratios(dependency_data: dict, iso3Code: str = None) -> dict:
    """
    Parse dependency ratios data from CIA World Factbook format.

    Handles nested structure:
    {
        "total dependency ratio": {"text": "53.7"},
        "youth dependency ratio": {"text": "28"},
        "elderly dependency ratio": {"text": "25.6"},
        "potential support ratio": {"text": "3.9 (2021 est.)"}
    }

    Args:
        dependency_data: Dictionary with nested structure
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured dependency ratios data
    """
    result = {
        "dependency_ratios": {
            "total": None,
            "youth": None,
            "elderly": None,
            "potential_support_ratio": None,
            "timestamp": None,
            "is_estimate": False
        },
        "dependency_ratios_note": ""
    }

    if not dependency_data or not isinstance(dependency_data, dict):
        return result

    # Helper to extract ratio value and year from text
    def extract_ratio(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False

        # Pattern: "53.7" or "3.9 (2021 est.)"
        num_match = re.search(r'([\d.]+)', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

        ratio = float(num_match.group(1)) if num_match else None
        year = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False

        return ratio, year, is_est

    # Field mappings
    field_map = {
        'total dependency ratio': 'total',
        'youth dependency ratio': 'youth',
        'elderly dependency ratio': 'elderly',
        'potential support ratio': 'potential_support_ratio'
    }

    for field_name, result_key in field_map.items():
        if field_name in dependency_data:
            field_data = dependency_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            ratio, year, is_est = extract_ratio(text)
            result["dependency_ratios"][result_key] = ratio
            if year and not result["dependency_ratios"]["timestamp"]:
                result["dependency_ratios"]["timestamp"] = year
                result["dependency_ratios"]["is_estimate"] = is_est

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Full data
    test1 = {
        "total dependency ratio": {"text": "53.7"},
        "youth dependency ratio": {"text": "28"},
        "elderly dependency ratio": {"text": "25.6"},
        "potential support ratio": {"text": "3.9 (2021 est.)"}
    }
    print("Test 1 - Full data:")
    print(parse_dependency_ratios(test1))
    print()

    # Test Case 2: Partial data
    test2 = {
        "total dependency ratio": {"text": "55.4"},
        "youth dependency ratio": {"text": "32.8"}
    }
    print("Test 2 - Partial data:")
    print(parse_dependency_ratios(test2))
