import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_net_migration_rate(migration_data: dict, iso3Code: str = None) -> dict:
    """
    Parse net migration rate data from CIA World Factbook format.

    Handles formats:
    1. Positive: "6.7 migrant(s)/1,000 population (2024 est.)"
    2. Negative: "-10.9 migrant(s)/1,000 population (2024 est.)"
    3. NA values

    Args:
        migration_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured net migration rate data:
        {
            "net_migration_rate": {
                "value": 6.7,
                "unit": "migrant(s)/1,000 population",
                "timestamp": "2024",
                "is_estimate": True
            },
            "net_migration_rate_note": ""
        }
    """
    result = {
        "net_migration_rate": {
            "value": None,
            "unit": "migrant(s)/1,000 population",
            "timestamp": None,
            "is_estimate": False
        },
        "net_migration_rate_note": ""
    }

    if not migration_data or not isinstance(migration_data, dict):
        return result

    text = migration_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "-10.9 migrant(s)/1,000 population (2024 est.)"
    PATTERN = re.compile(
        r'(-?[\d.]+)\s*migrants?\(?s?\)?/1,000\s*population\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["net_migration_rate"]["value"] = float(match.group(1))
        if match.group(2):
            result["net_migration_rate"]["timestamp"] = match.group(2)
        if match.group(3):
            result["net_migration_rate"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number (including negative)
        num_match = re.search(r'(-?[\d.]+)', text)
        if num_match:
            result["net_migration_rate"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for net migration rate: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Positive value
    test1 = {"text": "6.7 migrant(s)/1,000 population (2024 est.)"}
    print("Test 1 - Positive value:")
    print(parse_net_migration_rate(test1))
    print()

    # Test Case 2: Negative value
    test2 = {"text": "-10.9 migrant(s)/1,000 population (2024 est.)"}
    print("Test 2 - Negative value:")
    print(parse_net_migration_rate(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_net_migration_rate(test3))
