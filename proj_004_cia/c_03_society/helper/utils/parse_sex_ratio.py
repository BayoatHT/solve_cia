import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_sex_ratio(sex_data: dict, iso3Code: str = None) -> dict:
    """
    Parse sex ratio data from CIA World Factbook format.

    Handles nested structure:
    {
        "at birth": {"text": "1.05 male(s)/female"},
        "0-14 years": {"text": "1.05 male(s)/female"},
        "15-64 years": {"text": "1 male(s)/female"},
        "65 years and over": {"text": "0.81 male(s)/female"},
        "total population": {"text": "0.97 male(s)/female (2024 est.)"}
    }

    Args:
        sex_data: Dictionary with nested structure
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured sex ratio data
    """
    result = {
        "sex_ratio": {
            "at_birth": None,
            "0_14_years": None,
            "15_64_years": None,
            "65_years_and_over": None,
            "total_population": None,
            "unit": "male(s)/female",
            "timestamp": None,
            "is_estimate": False
        },
        "sex_ratio_note": ""
    }

    if not sex_data or not isinstance(sex_data, dict):
        return result

    # Helper to extract ratio and year from text
    def extract_ratio(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False

        # Pattern: "1.05 male(s)/female" or "0.97 male(s)/female (2024 est.)"
        ratio_match = re.search(r'([\d.]+)\s*male', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

        ratio = float(ratio_match.group(1)) if ratio_match else None
        year = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False

        return ratio, year, is_est

    # Field mappings
    field_map = {
        'at birth': 'at_birth',
        '0-14 years': '0_14_years',
        '15-64 years': '15_64_years',
        '65 years and over': '65_years_and_over',
        'total population': 'total_population'
    }

    for field_name, result_key in field_map.items():
        if field_name in sex_data:
            field_data = sex_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            ratio, year, is_est = extract_ratio(text)
            result["sex_ratio"][result_key] = ratio
            if year and not result["sex_ratio"]["timestamp"]:
                result["sex_ratio"]["timestamp"] = year
                result["sex_ratio"]["is_estimate"] = is_est

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Full data
    test1 = {
        "at birth": {"text": "1.05 male(s)/female"},
        "0-14 years": {"text": "1.05 male(s)/female"},
        "15-64 years": {"text": "1 male(s)/female"},
        "65 years and over": {"text": "0.81 male(s)/female"},
        "total population": {"text": "0.97 male(s)/female (2024 est.)"}
    }
    print("Test 1 - Full data:")
    print(parse_sex_ratio(test1))
