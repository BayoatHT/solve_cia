import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_budget_surplus_deficit(iso3Code: str) -> dict:
    """
    Parse budget surplus/deficit data from CIA World Factbook for a given country.

    This parser extracts budget surplus/deficit information.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured budget surplus/deficit data:
        {
            "budget_surplus_deficit": str
        }

    Examples:
        >>> data = parse_budget_surplus_deficit('USA')
        >>> 'budget_surplus_deficit' in data
        True

        >>> data = parse_budget_surplus_deficit('DEU')
        >>> data.get('budget_surplus_deficit') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Budget surplus (+) or deficit (-)
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Budget surplus (+) or deficit (-)', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Clean the text value and store it in the result dictionary
        result['budget_surplus_deficit'] = clean_text(pass_data.get("text", ""))
    except Exception as e:
        logger.error(f"Error parsing budget_surplus_deficit for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_budget_surplus_deficit with real country data."""
    print("="*60)
    print("Testing parse_budget_surplus_deficit across countries")
    print("="*60)

    test_countries = ['USA', 'DEU', 'CHN', 'FRA', 'JPN', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_budget_surplus_deficit(iso3)

            if result.get('budget_surplus_deficit'):
                surplus = result['budget_surplus_deficit']
                print(f"  Budget Surplus/Deficit: {surplus}")
            else:
                print("  No budget surplus/deficit data found")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
