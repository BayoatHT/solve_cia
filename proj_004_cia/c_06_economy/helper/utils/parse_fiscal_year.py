import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_fiscal_year(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse fiscal year data from CIA World Factbook for a given country.

    This parser extracts fiscal year information such as:
    - Fiscal year period (calendar year, 1 April - 31 March, etc.)
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured fiscal year data:
        {
            "fiscal_year": str,
            "fiscal_year_note": str
        }

    Examples:
        >>> data = parse_fiscal_year('USA')
        >>> 'fiscal_year' in data
        True

        >>> data = parse_fiscal_year('IND')
        >>> data.get('fiscal_year') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Fiscal year
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Fiscal year', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['fiscal_year'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['fiscal_year_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing fiscal_year for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_fiscal_year with real country data."""
    print("="*60)
    print("Testing parse_fiscal_year across countries")
    print("="*60)

    test_countries = ['USA', 'IND', 'GBR', 'AUS', 'JPN', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_fiscal_year(iso3)

            if result.get('fiscal_year'):
                print(f"  Fiscal Year: {result['fiscal_year']}")
            else:
                print("  No fiscal year data found")

            if result.get('fiscal_year_note'):
                note = result['fiscal_year_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
