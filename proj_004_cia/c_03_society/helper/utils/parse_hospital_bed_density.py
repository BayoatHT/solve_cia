import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_hospital_bed_density(hospital_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse hospital bed density from CIA World Factbook format.

    Handles formats:
    1. Standard: "2.9 beds/1,000 population (2017)"
    2. NA values

    Args:
        hospital_data: Dictionary with 'text' key
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured hospital bed density data:
        {
            "hospital_bed_density": {
                "value": 2.9,
                "unit": "beds/1,000 population",
                "timestamp": "2017",
                "is_estimate": False
            },
            "hospital_bed_density_note": ""
        }
    """
    if return_original:
        return hospital_data

    result = {
        "hospital_bed_density": {
            "value": None,
            "unit": "beds/1,000 population",
            "timestamp": None,
            "is_estimate": False
        },
        "hospital_bed_density_note": ""
    }

    if not hospital_data or not isinstance(hospital_data, dict):
        return result

    text = hospital_data.get('text', '').strip()

    # Handle NA or empty
    if not text or text.upper() == 'NA':
        return result

    # Pattern: "2.9 beds/1,000 population (2017)"
    PATTERN = re.compile(
        r'([\d.]+)\s*beds?/1,000\s*population\s*(?:\(([\d]{4})\s*(est\.?)?\))?'
    )

    match = PATTERN.search(text)
    if match:
        result["hospital_bed_density"]["value"] = float(match.group(1))
        if match.group(2):
            result["hospital_bed_density"]["timestamp"] = match.group(2)
        if match.group(3):
            result["hospital_bed_density"]["is_estimate"] = True
    else:
        # Fallback: try to extract just a number
        num_match = re.search(r'([\d.]+)', text)
        if num_match:
            result["hospital_bed_density"]["value"] = float(num_match.group(1))
            logger.warning(f"Partial parse for hospital bed density: {text[:50]}...")

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format
    test1 = {"text": "2.9 beds/1,000 population (2017)"}
    print("Test 1 - Standard format:")
    print(parse_hospital_bed_density(test1))
    print()

    # Test Case 2: High value
    test2 = {"text": "8 beds/1,000 population (2019)"}
    print("Test 2 - High value:")
    print(parse_hospital_bed_density(test2))
    print()

    # Test Case 3: NA
    test3 = {"text": "NA"}
    print("Test 3 - NA:")
    print(parse_hospital_bed_density(test3))
