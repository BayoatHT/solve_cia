import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_population_below_poverty(iso3Code: str) -> dict:
    """
    Parse population below poverty line data from CIA World Factbook for a given country.

    This parser extracts poverty line information including:
    - Poverty rate text (percentage with year)
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured poverty line data:
        {
            "population_below_poverty": str,
            "population_below_poverty_note": str
        }

    Examples:
        >>> data = parse_population_below_poverty('USA')
        >>> 'population_below_poverty' in data
        True

        >>> data = parse_population_below_poverty('IND')
        >>> data.get('population_below_poverty') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Population below poverty line
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Population below poverty line', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['population_below_poverty'] = clean_text(text)
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['population_below_poverty_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing population_below_poverty for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_population_below_poverty with real country data."""
    print("="*60)
    print("Testing parse_population_below_poverty across countries")
    print("="*60)

    test_countries = ['USA', 'IND', 'BRA', 'CHN', 'ZAF', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_population_below_poverty(iso3)

            if result.get('population_below_poverty'):
                poverty = result['population_below_poverty']
                print(f"  Poverty Rate: {poverty}")
            else:
                print("  No poverty line data found")

            if result.get('population_below_poverty_note'):
                note = result['population_below_poverty_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
