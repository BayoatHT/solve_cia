import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_literacy(literacy_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse literacy rate data from CIA World Factbook format.

    Handles nested structure:
    {
        "definition": {"text": "age 15 and over can read and write"},
        "total population": {"text": "67%"},
        "male": {"text": "71.8%"},
        "female": {"text": "62.2% (2021)"}
    }

    Args:
        literacy_data: Dictionary with nested structure
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured literacy data
    """
    if return_original:
        return literacy_data

    result = {
        "literacy": {
            "definition": None,
            "total": None,
            "male": None,
            "female": None,
            "timestamp": None,
            "is_estimate": False
        },
        "literacy_note": ""
    }

    if not literacy_data or not isinstance(literacy_data, dict):
        return result

    # Extract definition
    if 'definition' in literacy_data:
        def_data = literacy_data['definition']
        if isinstance(def_data, dict):
            result["literacy"]["definition"] = def_data.get('text', '').strip()
        elif isinstance(def_data, str):
            result["literacy"]["definition"] = def_data.strip()

    # Helper to extract percentage and year from text
    def extract_percentage(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False

        # Pattern: "67%" or "62.2% (2021)" or "62.2% (2021 est.)"
        pct_match = re.search(r'([\d.]+)%', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

        percentage = float(pct_match.group(1)) if pct_match else None
        year = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False

        return percentage, year, is_est

    # Extract total population
    if 'total population' in literacy_data:
        total_data = literacy_data['total population']
        text = total_data.get('text', '') if isinstance(total_data, dict) else str(total_data)
        pct, year, is_est = extract_percentage(text)
        result["literacy"]["total"] = pct
        if year:
            result["literacy"]["timestamp"] = year
            result["literacy"]["is_estimate"] = is_est

    # Extract male
    if 'male' in literacy_data:
        male_data = literacy_data['male']
        text = male_data.get('text', '') if isinstance(male_data, dict) else str(male_data)
        pct, year, is_est = extract_percentage(text)
        result["literacy"]["male"] = pct
        if year and not result["literacy"]["timestamp"]:
            result["literacy"]["timestamp"] = year
            result["literacy"]["is_estimate"] = is_est

    # Extract female
    if 'female' in literacy_data:
        female_data = literacy_data['female']
        text = female_data.get('text', '') if isinstance(female_data, dict) else str(female_data)
        pct, year, is_est = extract_percentage(text)
        result["literacy"]["female"] = pct
        if year and not result["literacy"]["timestamp"]:
            result["literacy"]["timestamp"] = year
            result["literacy"]["is_estimate"] = is_est

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Full data
    test1 = {
        "definition": {"text": "age 15 and over can read and write"},
        "total population": {"text": "67%"},
        "male": {"text": "71.8%"},
        "female": {"text": "62.2% (2021)"}
    }
    print("Test 1 - Full data:")
    print(parse_literacy(test1))
    print()

    # Test Case 2: NA values
    test2 = {
        "total population": {"text": "NA"},
        "male": {"text": "NA"},
        "female": {"text": "NA"}
    }
    print("Test 2 - NA values:")
    print(parse_literacy(test2))
    print()

    # Test Case 3: Empty
    print("Test 3 - Empty:")
    print(parse_literacy({}))
