import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_school_life_expectancy(school_data: dict, iso3Code: str = None) -> dict:
    """
    Parse school life expectancy data from CIA World Factbook format.

    Handles nested structure:
    {
        "total": {"text": "16 years"},
        "male": {"text": "16 years"},
        "female": {"text": "17 years (2020)"}
    }

    Args:
        school_data: Dictionary with nested structure
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured school life expectancy data
    """
    result = {
        "school_life_expectancy": {
            "total": None,
            "male": None,
            "female": None,
            "unit": "years",
            "timestamp": None,
            "is_estimate": False
        },
        "school_life_expectancy_note": ""
    }

    if not school_data or not isinstance(school_data, dict):
        return result

    # Helper to extract years and timestamp from text
    def extract_years(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False

        # Pattern: "16 years" or "17 years (2020)" or "17 years (2020 est.)"
        years_match = re.search(r'(\d+)\s*years?', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

        years = int(years_match.group(1)) if years_match else None
        timestamp = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False

        return years, timestamp, is_est

    # Extract total
    if 'total' in school_data:
        total_data = school_data['total']
        text = total_data.get('text', '') if isinstance(total_data, dict) else str(total_data)
        years, timestamp, is_est = extract_years(text)
        result["school_life_expectancy"]["total"] = years
        if timestamp:
            result["school_life_expectancy"]["timestamp"] = timestamp
            result["school_life_expectancy"]["is_estimate"] = is_est

    # Extract male
    if 'male' in school_data:
        male_data = school_data['male']
        text = male_data.get('text', '') if isinstance(male_data, dict) else str(male_data)
        years, timestamp, is_est = extract_years(text)
        result["school_life_expectancy"]["male"] = years
        if timestamp and not result["school_life_expectancy"]["timestamp"]:
            result["school_life_expectancy"]["timestamp"] = timestamp
            result["school_life_expectancy"]["is_estimate"] = is_est

    # Extract female
    if 'female' in school_data:
        female_data = school_data['female']
        text = female_data.get('text', '') if isinstance(female_data, dict) else str(female_data)
        years, timestamp, is_est = extract_years(text)
        result["school_life_expectancy"]["female"] = years
        if timestamp and not result["school_life_expectancy"]["timestamp"]:
            result["school_life_expectancy"]["timestamp"] = timestamp
            result["school_life_expectancy"]["is_estimate"] = is_est

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Full data
    test1 = {
        "total": {"text": "16 years"},
        "male": {"text": "16 years"},
        "female": {"text": "17 years (2020)"}
    }
    print("Test 1 - Full data:")
    print(parse_school_life_expectancy(test1))
    print()

    # Test Case 2: With estimate
    test2 = {
        "total": {"text": "11 years"},
        "male": {"text": "10 years"},
        "female": {"text": "11 years (2020 est.)"}
    }
    print("Test 2 - With estimate:")
    print(parse_school_life_expectancy(test2))
    print()

    # Test Case 3: Empty
    print("Test 3 - Empty:")
    print(parse_school_life_expectancy({}))
