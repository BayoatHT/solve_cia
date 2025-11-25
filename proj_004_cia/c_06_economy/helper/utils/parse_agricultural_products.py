import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_agricultural_products(iso3Code: str) -> dict:
    """
    Parse agricultural products data from CIA World Factbook for a given country.

    This parser extracts agricultural products information including:
    - List of agricultural products
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured agricultural products data:
        {
            "agricultural_products": [str],
            "agricultural_products_year": str,
            "agricultural_products_note": str
        }

    Examples:
        >>> data = parse_agricultural_products('USA')
        >>> isinstance(data.get('agricultural_products', []), list)
        True

        >>> data = parse_agricultural_products('CHN')
        >>> len(data.get('agricultural_products', [])) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Agricultural products
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Agricultural products', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Extract text for products and note, if available
        text = pass_data.get("text", "")
        note = pass_data.get("note", "")

        if text:
            # Check if the text ends with a date in parentheses and extract it
            date_match = re.search(r"\((\d{4})\)$", text)
            if date_match:
                result["agricultural_products_year"] = date_match.group(1)
                # Remove the date portion from the text
                text = text[:date_match.start()].strip()

            # Split the text by commas for agricultural products
            products = [item.strip() for item in text.split(",") if item.strip()]
            if products:
                result["agricultural_products"] = products

        # Clean the note text if present
        if note:
            result["agricultural_products_note"] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing agricultural_products for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_agricultural_products with real country data."""
    print("="*60)
    print("Testing parse_agricultural_products across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'FRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_agricultural_products(iso3)

            if result.get('agricultural_products'):
                products = result['agricultural_products']
                year = result.get('agricultural_products_year', '')
                year_str = f" ({year})" if year else ""

                print(f"  Products{year_str}: {len(products)} items")
                # Show first 5 products
                display_products = products[:5]
                print(f"    {', '.join(display_products)}", end="")
                if len(products) > 5:
                    print(f" ... and {len(products) - 5} more")
                else:
                    print()
            else:
                print("  No agricultural products data found")

            if result.get('agricultural_products_note'):
                note = result['agricultural_products_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
