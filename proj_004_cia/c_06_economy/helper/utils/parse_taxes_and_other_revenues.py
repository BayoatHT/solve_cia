import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_taxes_and_other_revenues(iso3Code: str) -> Dict[str, Any]:
    """
    Parse taxes and other revenues data from CIA World Factbook for a given country.

    This parser extracts taxes and revenues information including:
    - Percentage of GDP
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured taxes and revenues data:
        {
            "taxes_revenues": {
                "value": float,
                "unit": str,
                "year": int
            },
            "taxes_revenues_note": str
        }

    Examples:
        >>> data = parse_taxes_and_other_revenues('USA')
        >>> 'taxes_revenues' in data
        True

        >>> data = parse_taxes_and_other_revenues('DEU')
        >>> data.get('taxes_revenues', {}).get('value') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Taxes and other revenues
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Taxes and other revenues', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Process 'text' field for percentage and year
        text = pass_data.get("text", "")
        match = re.match(r"([\d.]+)%\s*\(of GDP\)\s*\((\d{4})", text)
        if match:
            result["taxes_revenues"] = {
                "value": float(match.group(1)),
                "unit": "% of GDP",
                "year": int(match.group(2))
            }
        elif text:
            logger.warning(f"Unexpected format in 'text' data: {text}")

        # Process 'note' field
        note = pass_data.get("note", "")
        if note:
            result["taxes_revenues_note"] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing taxes_and_other_revenues for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_taxes_and_other_revenues with real country data."""
    print("="*60)
    print("Testing parse_taxes_and_other_revenues across countries")
    print("="*60)

    test_countries = ['USA', 'DEU', 'FRA', 'CHN', 'IND', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_taxes_and_other_revenues(iso3)

            if result.get('taxes_revenues'):
                taxes = result['taxes_revenues']
                value = taxes.get('value')
                year = taxes.get('year', '')
                print(f"  Taxes/Revenues: {value}% of GDP ({year})")
            else:
                print("  No taxes/revenues data found")

            if result.get('taxes_revenues_note'):
                note = result['taxes_revenues_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
