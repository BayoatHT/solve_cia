import re
import logging
from typing import Dict, List, Optional, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_age_structure(age_structure_data: dict, iso3Code: str = None) -> dict:
    """
    Parse age structure data from CIA World Factbook format.

    Handles ALL format variations found across 262 countries:
    1. Standard with year in middle: "16.7% (2024 est.) (male 322,941/female 495,374)"
    2. Standard without year: "20.6% (male 520,091/female 489,882)"
    3. Year at end: "4.1% (male 11,802/female 14,946) (2020 est.)"
    4. Percentage only with year: "17.3% (2021)"
    5. Percentage only without year: "21.2%"
    6. NA values: "NA"

    Bracket variations:
    - Standard 3-bracket: 0-14, 15-64, 65+
    - Extended 5-bracket (wi.json): 0-14, 15-24, 25-54, 55-64, 65+

    Args:
        age_structure_data: Dictionary with age bracket keys and text values
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured age data:
        {
            "age_structure": [...],
            "age_structure_note": ""
        }
    """
    result = {
        "age_structure": [],
        "age_structure_note": ""
    }

    if not age_structure_data or not isinstance(age_structure_data, dict):
        return result

    # Define age bracket mapping for min/max extraction
    AGE_BRACKET_MAP = {
        "0-14 years": {"range": "0-14", "min": 0, "max": 14},
        "15-24 years": {"range": "15-24", "min": 15, "max": 24},
        "25-54 years": {"range": "25-54", "min": 25, "max": 54},
        "55-64 years": {"range": "55-64", "min": 55, "max": 64},
        "15-64 years": {"range": "15-64", "min": 15, "max": 64},
        "65 years and over": {"range": "65+", "min": 65, "max": None},
    }

    # Regex patterns for different formats
    # Pattern 1: Percentage with year in middle, then gender breakdown
    # Example: "16.7% (2024 est.) (male 322,941/female 495,374)"
    PATTERN_YEAR_MIDDLE = re.compile(
        r'([\d.]+)%\s*\((\d{4})\s*(?:est\.?)?\)\s*\(male\s+([\d,]+)/female\s+([\d,]+)\)'
    )

    # Pattern 2: Percentage with gender breakdown, year at end
    # Example: "4.1% (male 11,802/female 14,946) (2020 est.)"
    PATTERN_YEAR_END = re.compile(
        r'([\d.]+)%\s*\(male\s+([\d,]+)/female\s+([\d,]+)\)\s*\((\d{4})\s*(?:est\.?)?\)'
    )

    # Pattern 3: Percentage with gender breakdown, no year
    # Example: "20.6% (male 520,091/female 489,882)"
    PATTERN_NO_YEAR = re.compile(
        r'([\d.]+)%\s*\(male\s+([\d,]+)/female\s+([\d,]+)\)'
    )

    # Pattern 4: Percentage only with year
    # Example: "17.3% (2021)"
    PATTERN_PCT_YEAR = re.compile(
        r'([\d.]+)%\s*\((\d{4})\)'
    )

    # Pattern 5: Percentage only
    # Example: "21.2%"
    PATTERN_PCT_ONLY = re.compile(
        r'^([\d.]+)%$'
    )

    def parse_count(count_str: str) -> Optional[int]:
        """Convert comma-separated number string to integer."""
        if not count_str:
            return None
        try:
            return int(count_str.replace(',', ''))
        except (ValueError, AttributeError):
            return None

    def parse_bracket(bracket_key: str, bracket_data: dict) -> Optional[dict]:
        """Parse a single age bracket."""
        if not isinstance(bracket_data, dict):
            return None

        text = bracket_data.get('text', '').strip()

        # Skip metadata entries (like 'count' fields)
        if bracket_key not in AGE_BRACKET_MAP:
            return None

        bracket_info = AGE_BRACKET_MAP[bracket_key]

        # Initialize result structure
        parsed = {
            "age_range": bracket_info["range"],
            "age_min": bracket_info["min"],
            "age_max": bracket_info["max"],
            "percentage": None,
            "male_count": None,
            "female_count": None,
            "total_count": None,
            "timestamp": None,
            "is_estimate": False
        }

        # Handle NA values
        if text.upper() == 'NA' or not text:
            parsed["data_available"] = False
            return parsed

        parsed["data_available"] = True

        # Try Pattern 1: Year in middle
        match = PATTERN_YEAR_MIDDLE.search(text)
        if match:
            parsed["percentage"] = float(match.group(1))
            parsed["timestamp"] = match.group(2)
            parsed["is_estimate"] = True
            parsed["male_count"] = parse_count(match.group(3))
            parsed["female_count"] = parse_count(match.group(4))
            if parsed["male_count"] and parsed["female_count"]:
                parsed["total_count"] = parsed["male_count"] + parsed["female_count"]
            return parsed

        # Try Pattern 2: Year at end
        match = PATTERN_YEAR_END.search(text)
        if match:
            parsed["percentage"] = float(match.group(1))
            parsed["male_count"] = parse_count(match.group(2))
            parsed["female_count"] = parse_count(match.group(3))
            parsed["timestamp"] = match.group(4)
            parsed["is_estimate"] = True
            if parsed["male_count"] and parsed["female_count"]:
                parsed["total_count"] = parsed["male_count"] + parsed["female_count"]
            return parsed

        # Try Pattern 3: No year, with gender breakdown
        match = PATTERN_NO_YEAR.search(text)
        if match:
            parsed["percentage"] = float(match.group(1))
            parsed["male_count"] = parse_count(match.group(2))
            parsed["female_count"] = parse_count(match.group(3))
            if parsed["male_count"] and parsed["female_count"]:
                parsed["total_count"] = parsed["male_count"] + parsed["female_count"]
            return parsed

        # Try Pattern 4: Percentage with year only
        match = PATTERN_PCT_YEAR.search(text)
        if match:
            parsed["percentage"] = float(match.group(1))
            parsed["timestamp"] = match.group(2)
            parsed["is_estimate"] = False  # No "est." marker
            return parsed

        # Try Pattern 5: Percentage only
        match = PATTERN_PCT_ONLY.search(text)
        if match:
            parsed["percentage"] = float(match.group(1))
            return parsed

        # Fallback: Try to extract at least the percentage
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            parsed["percentage"] = float(pct_match.group(1))
            # Check for year anywhere in text
            year_match = re.search(r'\((\d{4})\s*(?:est\.?)?\)', text)
            if year_match:
                parsed["timestamp"] = year_match.group(1)
                parsed["is_estimate"] = 'est' in text.lower()
            logger.warning(f"Partial parse for {bracket_key}: {text[:50]}...")
            return parsed

        logger.warning(f"Could not parse age bracket {bracket_key}: {text[:50]}...")
        return parsed

    # Process each age bracket
    for bracket_key, bracket_data in age_structure_data.items():
        # Skip non-bracket keys (like 'count', 'population pyramid')
        if bracket_key not in AGE_BRACKET_MAP:
            continue

        parsed_bracket = parse_bracket(bracket_key, bracket_data)
        if parsed_bracket:
            result["age_structure"].append(parsed_bracket)

    # Sort brackets by age_min for consistent output
    result["age_structure"].sort(key=lambda x: x.get("age_min", 0))

    return result


# Example usage and testing
if __name__ == "__main__":
    # Test Case 1: Standard format (most common)
    test1 = {
        "0-14 years": {"text": "18.1% (male 31,618,532/female 30,254,223)"},
        "15-64 years": {"text": "63.4% (male 108,553,822/female 108,182,491)"},
        "65 years and over": {"text": "18.5% (2024 est.) (male 28,426,426/female 34,927,914)"}
    }
    print("Test 1 - Standard format:")
    print(parse_age_structure(test1))
    print()

    # Test Case 2: Year at end (wi.json format)
    test2 = {
        "0-14 years": {"text": "36.29% (male 119,719/female 116,997)"},
        "15-24 years": {"text": "19.44% (male 63,852/female 62,954)"},
        "25-54 years": {"text": "34.9% (male 112,301/female 115,313)"},
        "55-64 years": {"text": "5.27% (male 16,095/female 18,292)"},
        "65 years and over": {"text": "4.1% (male 11,802/female 14,946) (2020 est.)"}
    }
    print("Test 2 - 5-bracket with year at end:")
    print(parse_age_structure(test2))
    print()

    # Test Case 3: Percentage only (ck.json format)
    test3 = {
        "0-14 years": {"text": "21.2%"},
        "15-64 years": {"text": "61.5%"},
        "65 years and over": {"text": "17.3% (2021)"}
    }
    print("Test 3 - Percentage only:")
    print(parse_age_structure(test3))
    print()

    # Test Case 4: NA values (ax.json format)
    test4 = {
        "0-14 years": {"text": "NA"},
        "15-64 years": {"text": "NA"},
        "65 years and over": {"text": "NA"}
    }
    print("Test 4 - NA values:")
    print(parse_age_structure(test4))
    print()

    # Test Case 5: Empty input
    print("Test 5 - Empty input:")
    print(parse_age_structure({}))
