import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_industrial_production(iso3Code: str, return_original: bool = False)-> Dict[str, Any]:
    """
    Parse industrial production growth rate data from CIA World Factbook for a given country.

    This parser extracts industrial production information including:
    - Growth rate percentage
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured industrial production data:
        {
            "industrial_production_growth_rate": {"value": float, "year": int, "unit": str},
            "industrial_production_growth_rate_note": str
        }

    Examples:
        >>> data = parse_industrial_production('USA')
        >>> 'industrial_production_growth_rate' in data
        True

        >>> data = parse_industrial_production('CHN')
        >>> data.get('industrial_production_growth_rate', {}).get('value') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Industrial production growth rate
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Industrial production growth rate', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Process the "text" field
        text = pass_data.get("text", "")
        if text:
            match = re.match(r"([-\d.]+)% \((\d{4}) est\.\)", text)
            if match:
                result["industrial_production_growth_rate"] = {
                    "value": float(match.group(1)),
                    "year": int(match.group(2)),
                    "unit": "%"
                }

        # Process the "note" field
        note = pass_data.get("note", "")
        if note:
            result["industrial_production_growth_rate_note"] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing industrial_production for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_industrial_production with real country data."""
    print("="*60)
    print("Testing parse_industrial_production across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'DEU', 'IND', 'BRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_industrial_production(iso3)

            if result.get('industrial_production_growth_rate'):
                prod = result['industrial_production_growth_rate']
                value = prod.get('value')
                year = prod.get('year', '')
                print(f"  Industrial Production Growth Rate: {value}% ({year})")
            else:
                print("  No industrial production data found")

            if result.get('industrial_production_growth_rate_note'):
                note = result['industrial_production_growth_rate_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
