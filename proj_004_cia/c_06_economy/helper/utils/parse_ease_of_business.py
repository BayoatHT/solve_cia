import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_ease_of_business(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse ease of doing business index data from CIA World Factbook for a given country.

    This parser extracts ease of business information.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured ease of business data:
        {
            "ease_of_business": str,
            "ease_of_business_note": str
        }

    Examples:
        >>> data = parse_ease_of_business('USA')
        >>> isinstance(data, dict)
        True

        >>> data = parse_ease_of_business('CHN')
        >>> isinstance(data, dict)
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Ease of Doing Business Index scores
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Ease of Doing Business Index scores', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['ease_of_business'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['ease_of_business_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing ease_of_business for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_ease_of_business with real country data."""
    print("="*60)
    print("Testing parse_ease_of_business across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_ease_of_business(iso3)

            if result.get('ease_of_business'):
                ease = result['ease_of_business']
                print(f"  Ease of Business: {ease[:80]}...")
            else:
                print("  No ease of business data found")

            if result.get('ease_of_business_note'):
                note = result['ease_of_business_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
