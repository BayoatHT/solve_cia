import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_household_income(iso3Code: str, return_original: bool = False)-> Dict[str, Any]:
    """
    Parse household income distribution data from CIA World Factbook for a given country.

    This parser extracts household income information including:
    - Income share for lowest 10%
    - Income share for highest 10%
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured household income data:
        {
            "house_income_lowest_10": {"value": float, "unit": str, "year": int},
            "house_income_highest_10": {"value": float, "unit": str, "year": int},
            "house_income_note": str
        }

    Examples:
        >>> data = parse_household_income('USA')
        >>> 'house_income_lowest_10' in data
        True

        >>> data = parse_household_income('BRA')
        >>> data.get('house_income_highest_10', {}).get('value') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Household income or consumption by percentage share
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Household income or consumption by percentage share', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Loop through each key-value pair in pass_data
        for key, value in pass_data.items():
            if key == "lowest 10%":
                # Extract percentage and year from "lowest 10%" text field
                text = value.get("text", "")
                match = re.match(r"([\d\.]+)% \((\d{4}) est.\)", text)
                if match:
                    result["house_income_lowest_10"] = {
                        "value": float(match.group(1)),
                        "unit": "%",
                        "year": int(match.group(2))
                    }

            elif key == "highest 10%":
                # Extract percentage and year from "highest 10%" text field
                text = value.get("text", "")
                match = re.match(r"([\d\.]+)% \((\d{4}) est.\)", text)
                if match:
                    result["house_income_highest_10"] = {
                        "value": float(match.group(1)),
                        "unit": "%",
                        "year": int(match.group(2))
                    }

            elif key == "note":
                # Clean and store the note
                result["house_income_note"] = clean_text(value)

    except Exception as e:
        logger.error(f"Error parsing household_income for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_household_income with real country data."""
    print("="*60)
    print("Testing parse_household_income across countries")
    print("="*60)

    test_countries = ['USA', 'BRA', 'ZAF', 'CHN', 'IND', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_household_income(iso3)

            if result.get('house_income_lowest_10'):
                lowest = result['house_income_lowest_10']
                year = lowest.get('year', '')
                print(f"  Lowest 10%: {lowest['value']}% ({year})")

            if result.get('house_income_highest_10'):
                highest = result['house_income_highest_10']
                print(f"  Highest 10%: {highest['value']}%")

            if not result.get('house_income_lowest_10') and not result.get('house_income_highest_10'):
                print("  No household income data found")

            if result.get('house_income_note'):
                note = result['house_income_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
