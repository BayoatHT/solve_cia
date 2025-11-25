import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_imports_partners(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse imports partners data from CIA World Factbook for a given country.

    This parser extracts imports partners information including:
    - List of trading partners with their percentage shares
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured imports partners data:
        {
            "imports_partners": {
                "partners": [{"country": str, "percentage": int}],
                "date": int
            },
            "imports_partners_note": str
        }

    Examples:
        >>> data = parse_imports_partners('USA')
        >>> 'imports_partners' in data
        True

        >>> data = parse_imports_partners('CHN')
        >>> len(data.get('imports_partners', {}).get('partners', [])) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Imports - partners
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Imports - partners', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Handle the 'note' key if it exists
        if "note" in pass_data:
            result["imports_partners_note"] = clean_text(pass_data.get("note", ""))

        # Parse the main text for partners and year
        text = pass_data.get("text", "")
        if text:
            # Check for year in parentheses at the end of the text
            match = re.search(r"\((\d{4})\)$", text)
            if match:
                # Extract and set the year
                result["imports_partners"] = {
                    "date": int(match.group(1))
                }
                # Remove the year from the main text
                partners_text = text[:match.start()].strip()
            else:
                result["imports_partners"] = {}
                partners_text = text

            # Split the remaining text by commas to get partner and percentage pairs
            partners_list = []
            for entry in partners_text.split(","):
                entry = entry.strip()
                # Match the pattern for 'Country %'
                partner_match = re.match(r"(.+?)\s(\d+)%", entry)
                if partner_match:
                    country = partner_match.group(1).strip()
                    percentage = int(partner_match.group(2))
                    partners_list.append(
                        {"country": country, "percentage": percentage})

            # Store the list of partners in the result
            result["imports_partners"]["partners"] = partners_list

    except Exception as e:
        logger.error(f"Error parsing imports_partners for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_imports_partners with real country data."""
    print("="*60)
    print("Testing parse_imports_partners across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_imports_partners(iso3)

            if result.get('imports_partners'):
                partners_data = result['imports_partners']
                partners = partners_data.get('partners', [])
                year = partners_data.get('date', '')
                year_str = f" ({year})" if year else ""

                print(f"  Import Partners{year_str}: {len(partners)} partners")
                # Show all partners
                for partner in partners:
                    country = partner.get('country', '')
                    percentage = partner.get('percentage', 0)
                    print(f"    {country}: {percentage}%")
            else:
                print("  No imports partners data found")

            if result.get('imports_partners_note'):
                note = result['imports_partners_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
