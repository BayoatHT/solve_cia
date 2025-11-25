import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_exchange_rates(iso3Code: str) -> dict:
    """
    Parse exchange rates data from CIA World Factbook for a given country.

    This parser extracts exchange rates information including:
    - Exchange rate text (historical multi-year data)
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured exchange rates data:
        {
            "exchange_rates": str,
            "exchange_rates_note": str
        }

    Examples:
        >>> data = parse_exchange_rates('GBR')
        >>> 'exchange_rates' in data
        True

        >>> data = parse_exchange_rates('JPN')
        >>> data.get('exchange_rates') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Exchange rates
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Exchange rates', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['exchange_rates'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['exchange_rates_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing exchange_rates for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_exchange_rates with real country data."""
    print("="*60)
    print("Testing parse_exchange_rates across countries")
    print("="*60)

    test_countries = ['USA', 'GBR', 'JPN', 'CHN', 'DEU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_exchange_rates(iso3)

            if result.get('exchange_rates'):
                rates = result['exchange_rates']
                # Show first 100 characters
                print(f"  Exchange Rates: {rates[:100]}...")
            else:
                print("  No exchange rates data found")

            if result.get('exchange_rates_note'):
                note = result['exchange_rates_note'][:80]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
