import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_obesity(obesity_data: dict, iso3Code: str = None) -> dict:
    """
    Parse obesity adult prevalence rate from CIA World Factbook format.

    Handles formats:
    1. Standard: "36.2% (2016)"
    2. NA values

    Args:
        obesity_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured obesity data:
        {
            "obesity_rate": {
                "value": 36.2,
                "unit": "%",
                "timestamp": "2016",
                "is_estimate": False
            },
            "obesity_rate_note": ""
        }
    """
    result = {
        "obesity_rate": {
            "value": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "obesity_rate_note": ""
    }

    if not obesity_data or not isinstance(obesity_data, dict):
        return result

    text = obesity_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "36.2% (2016)" or "36.2% (2016 est.)"
    PATTERN = re.compile(
        r'([\d.]+)%\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["obesity_rate"]["value"] = float(match.group(1))
        if match.group(2):
            result["obesity_rate"]["timestamp"] = match.group(2)
        if match.group(3):
            result["obesity_rate"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number
        num_match = re.search(r'([\d.]+)', text)
        if num_match:
            result["obesity_rate"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for obesity rate: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "36.2% (2016)"}
    print("Test 1 - Standard format:")
    print(parse_obesity(test1))
    print()

    # Test Case 2: With estimate
    test2 = {"text": "21.7% (2016 est.)"}
    print("Test 2 - With estimate:")
    print(parse_obesity(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_obesity(test3))
