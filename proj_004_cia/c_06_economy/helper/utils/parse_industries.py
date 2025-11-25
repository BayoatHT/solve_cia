import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_industries(iso3Code: str) -> dict:
    """
    Parse industries data from CIA World Factbook for a given country.

    This parser extracts industries information including:
    - List of industries (semicolon or comma separated)
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured industries data:
        {
            "industries": [str],
            "industries_note": str
        }

    Examples:
        >>> data = parse_industries('USA')
        >>> isinstance(data.get('industries', []), list)
        True

        >>> data = parse_industries('CHN')
        >>> len(data.get('industries', [])) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Industries
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Industries', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Process text field with parse_text_to_list if available
        text = pass_data.get("text", "")
        if text:
            industries = parse_text_to_list(text)
            if industries:
                result["industries"] = industries

        # Process note field with clean_text if available
        note = pass_data.get("note", "")
        if note:
            result["industries_note"] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing industries for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_industries with real country data."""
    print("="*60)
    print("Testing parse_industries across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'DEU', 'JPN', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_industries(iso3)

            if result.get('industries'):
                industries = result['industries']
                print(f"  Industries: {len(industries)} items")
                # Show first 5 industries
                display_industries = industries[:5]
                print(f"    {', '.join(display_industries)}", end="")
                if len(industries) > 5:
                    print(f" ... and {len(industries) - 5} more")
                else:
                    print()
            else:
                print("  No industries data found")

            if result.get('industries_note'):
                note = result['industries_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
