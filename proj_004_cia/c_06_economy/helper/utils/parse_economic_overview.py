import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_economic_overview(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse economic overview data from CIA World Factbook for a given country.

    This parser extracts economic overview text information.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with economic overview text:
        {
            "economic_overview": str
        }

    Examples:
        >>> data = parse_economic_overview('USA')
        >>> 'economic_overview' in data
        True

        >>> data = parse_economic_overview('CHN')
        >>> len(data.get('economic_overview', '')) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Economic overview
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Economic overview', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Clean the text value and store it in the result dictionary
        text = pass_data.get("text", "")
        if text:
            result['economic_overview'] = clean_text(text)
    except Exception as e:
        logger.error(f"Error parsing economic_overview for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_economic_overview with real country data."""
    print("="*60)
    print("Testing parse_economic_overview across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'DEU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_economic_overview(iso3)

            if result.get('economic_overview'):
                overview = result['economic_overview']
                # Show first 150 characters
                print(f"  Economic Overview: {overview[:150]}...")
            else:
                print("  No economic overview data found")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
