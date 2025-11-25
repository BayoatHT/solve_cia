import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_exports_partners(iso3Code: str) -> dict:
    """
    Parse exports partners data from CIA World Factbook for a given country.

    This parser extracts exports partners information including:
    - List of trading partners with their percentage shares
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured exports partners data:
        {
            "exports_partners": {
                "partners": [{"country": str, "percentage": int}],
                "date": int
            },
            "exports_partners_note": str
        }

    Examples:
        >>> data = parse_exports_partners('USA')
        >>> 'exports_partners' in data
        True

        >>> data = parse_exports_partners('CHN')
        >>> len(data.get('exports_partners', {}).get('partners', [])) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Exports - partners
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Exports - partners', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Handle the 'note' key if it exists
        if "note" in pass_data:
            result["exports_partners_note"] = clean_text(pass_data.get("note", ""))

        # Parse the main text for partners and year
        text = pass_data.get("text", "")
        if text:
            # Check for year in parentheses at the end of the text
            match = re.search(r"\((\d{4})\)$", text)
            if match:
                # Extract and set the year
                result["exports_partners"] = {
                    "date": int(match.group(1))
                }
                # Remove the year from the main text
                partners_text = text[:match.start()].strip()
            else:
                result["exports_partners"] = {}
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
            result["exports_partners"]["partners"] = partners_list

    except Exception as e:
        logger.error(f"Error parsing exports_partners for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_exports_partners with real country data."""
    print("="*60)
    print("Testing parse_exports_partners across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_exports_partners(iso3)

            if result.get('exports_partners'):
                partners_data = result['exports_partners']
                partners = partners_data.get('partners', [])
                year = partners_data.get('date', '')
                year_str = f" ({year})" if year else ""

                print(f"  Export Partners{year_str}: {len(partners)} partners")
                # Show all partners
                for partner in partners:
                    country = partner.get('country', '')
                    percentage = partner.get('percentage', 0)
                    print(f"    {country}: {percentage}%")
            else:
                print("  No exports partners data found")

            if result.get('exports_partners_note'):
                note = result['exports_partners_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
