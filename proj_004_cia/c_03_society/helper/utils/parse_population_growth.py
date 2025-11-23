import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_population_growth(pop_growth_data: dict, iso3Code: str = None) -> dict:
    """
    Parse population growth rate data from CIA World Factbook format.

    Handles formats:
    1. Positive: "1.68% (2024 est.)"
    2. Negative: "-0.5% (2024 est.)"
    3. NA values

    Args:
        pop_growth_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured population growth data:
        {
            "population_growth_rate": {
                "value": 1.68,
                "unit": "%",
                "timestamp": "2024",
                "is_estimate": True
            },
            "population_growth_rate_note": ""
        }
    """
    result = {
        "population_growth_rate": {
            "value": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "population_growth_rate_note": ""
    }

    if not pop_growth_data or not isinstance(pop_growth_data, dict):
        return result

    text = pop_growth_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "-0.5% (2024 est.)"
    PATTERN = re.compile(
        r'(-?[\d.]+)%\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["population_growth_rate"]["value"] = float(match.group(1))
        if match.group(2):
            result["population_growth_rate"]["timestamp"] = match.group(2)
        if match.group(3):
            result["population_growth_rate"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number (including negative)
        num_match = re.search(r'(-?[\d.]+)', text)
        if num_match:
            result["population_growth_rate"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for population growth: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Positive value
    test1 = {"text": "1.68% (2024 est.)"}
    print("Test 1 - Positive value:")
    print(parse_population_growth(test1))
    print()

    # Test Case 2: Negative value
    test2 = {"text": "-0.5% (2024 est.)"}
    print("Test 2 - Negative value:")
    print(parse_population_growth(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_population_growth(test3))
