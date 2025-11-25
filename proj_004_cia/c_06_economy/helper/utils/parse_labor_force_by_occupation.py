import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_labor_force_by_occupation(iso3Code: str) -> Dict[str, Any]:
    """
    Parse labor force by occupation data from CIA World Factbook for a given country.

    This parser extracts labor force distribution by occupation including:
    - Agriculture, industry, services percentages
    - Year of data

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured labor force occupation data:
        {
            "labor_force_agriculture": {"percentage": float, "year": int},
            "labor_force_industry": {"percentage": float, "year": int},
            "labor_force_services": {"percentage": float, "year": int},
            ...
        }

    Examples:
        >>> data = parse_labor_force_by_occupation('USA')
        >>> 'labor_force_agriculture' in data or 'labor_force_industry' in data
        True

        >>> data = parse_labor_force_by_occupation('IND')
        >>> len(data) > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Labor force - by occupation
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Labor force - by occupation', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        for key, value in pass_data.items():
            # Define the base key name based on the occupation
            base_key = f"labor_force_{key.replace(' ', '_').lower()}"

            # Extract the text value
            text = value.get("text", "")

            # Extract percentage and year if available
            match = re.match(r"([\d.]+)%(?: \((\d{4}) est\.\))?", text)
            if match:
                percentage = float(match.group(1))
                year = int(match.group(2)) if match.group(2) else ""
                result[base_key] = {
                    "percentage": percentage,
                    "year": year
                }
            else:
                logger.warning(
                    f"Unexpected format in 'text' data for {key}: {text}")

    except Exception as e:
        logger.error(f"Error parsing labor_force_by_occupation for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_labor_force_by_occupation with real country data."""
    print("="*60)
    print("Testing parse_labor_force_by_occupation across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'BRA', 'DEU', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_labor_force_by_occupation(iso3)

            if result:
                for key, value in result.items():
                    sector = key.replace('labor_force_', '').replace('_', ' ').title()
                    year = value.get('year', '')
                    year_str = f" ({year})" if year else ""
                    print(f"  {sector}: {value['percentage']}%{year_str}")
            else:
                print("  No labor force occupation data found")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
