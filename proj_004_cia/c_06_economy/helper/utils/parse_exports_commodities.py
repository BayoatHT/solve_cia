import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_exports_commodities(iso3Code: str) -> dict:
    """
    Parse exports commodities data from CIA World Factbook for a given country.

    This parser extracts exports commodities information including:
    - List of major export commodities
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured exports commodities data:
        {
            "exports_commodities": {
                "commodities": [str],
                "date": int
            },
            "exports_commodities_note": str
        }

    Examples:
        >>> data = parse_exports_commodities('USA')
        >>> 'exports_commodities' in data
        True

        >>> data = parse_exports_commodities('CHN')
        >>> len(data.get('exports_commodities', {}).get('commodities', [])) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Exports - commodities
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Exports - commodities', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Handle the 'note' key if it exists
        if "note" in pass_data:
            result["exports_commodities_note"] = clean_text(
                pass_data.get("note", ""))

        # Parse the main text for commodities and date
        text = pass_data.get("text", "")
        if text:
            # Check for year in parentheses at the end of the text
            # Handle formats like "(2022)", "(2012 est.)", or no year at all
            match = re.search(r"\((\d{4})(?:\s*est\.?)?\)\s*$", text)
            if match:
                year = int(match.group(1))
                # Remove the year from the main text
                commodities_text = text[:match.start()].strip()
            else:
                year = None
                commodities_text = text

            # Split the remaining text by commas to get commodities list
            commodities_list = [commodity.strip() for commodity in commodities_text.split(
                ",") if commodity.strip()]

            # Build the result dict (always create the dict first)
            result["exports_commodities"] = {
                "commodities": commodities_list
            }
            if year:
                result["exports_commodities"]["date"] = year

    except Exception as e:
        logger.error(f"Error parsing exports_commodities for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_exports_commodities with real country data."""
    print("="*60)
    print("Testing parse_exports_commodities across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_exports_commodities(iso3)

            if result.get('exports_commodities'):
                commodities_data = result['exports_commodities']
                commodities = commodities_data.get('commodities', [])
                year = commodities_data.get('date', '')
                year_str = f" ({year})" if year else ""

                print(f"  Export Commodities{year_str}: {len(commodities)} items")
                # Show first 5 commodities
                display_commodities = commodities[:5]
                print(f"    {', '.join(display_commodities)}", end="")
                if len(commodities) > 5:
                    print(f" ... and {len(commodities) - 5} more")
                else:
                    print()
            else:
                print("  No exports commodities data found")

            if result.get('exports_commodities_note'):
                note = result['exports_commodities_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
