import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_youth_unemployment_rate(iso3Code: str) -> dict:
    """
    Parse youth unemployment rate data from CIA World Factbook for a given country.

    This parser extracts youth unemployment information including:
    - Total, male, and female unemployment rates
    - Year of data
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured youth unemployment data:
        {
            "youth_unemployment_total": {"value": float, "year": int},
            "youth_unemployment_male": {"value": float, "year": int},
            "youth_unemployment_female": {"value": float, "year": int},
            "youth_unemployment_note": str
        }

    Examples:
        >>> data = parse_youth_unemployment_rate('USA')
        >>> 'youth_unemployment_total' in data
        True

        >>> data = parse_youth_unemployment_rate('ZAF')
        >>> data.get('youth_unemployment_total', {}).get('value') is not None
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Youth unemployment rate (ages 15-24)
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Youth unemployment rate (ages 15-24)', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Define keys to process
        categories = {
            "total": "youth_unemployment_total",
            "male": "youth_unemployment_male",
            "female": "youth_unemployment_female"
        }

        # Parse each category
        for key, result_key in categories.items():
            if key in pass_data:
                text = pass_data[key].get("text", "")
                # Handle formats like "45.4% (2023 est.)" or just "17.5%"
                match = re.match(r"([\d.]+)%(?:\s*\((\d{4}))?", text)
                if match:
                    result[result_key] = {
                        "value": float(match.group(1)),
                        "year": int(match.group(2)) if match.group(2) else None
                    }
                elif text and text.upper() != 'NA':
                    # Only warn if there's actual text that couldn't be parsed (not NA)
                    logger.warning(f"Unexpected format in '{key}' data: {text}")

        # Handle 'note' if present
        if "note" in pass_data:
            result["youth_unemployment_note"] = clean_text(pass_data["note"])

    except Exception as e:
        logger.error(f"Error parsing youth_unemployment_rate for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_youth_unemployment_rate with real country data."""
    print("="*60)
    print("Testing parse_youth_unemployment_rate across countries")
    print("="*60)

    test_countries = ['ZAF', 'ESP', 'GRC', 'ITA', 'FRA', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_youth_unemployment_rate(iso3)

            if result.get('youth_unemployment_total'):
                total = result['youth_unemployment_total']
                year = total.get('year', 'N/A')
                print(f"  Total Youth Unemployment: {total['value']}% ({year})")

            if result.get('youth_unemployment_male'):
                male = result['youth_unemployment_male']
                print(f"  Male: {male['value']}%")

            if result.get('youth_unemployment_female'):
                female = result['youth_unemployment_female']
                print(f"  Female: {female['value']}%")

            if not result.get('youth_unemployment_total'):
                print("  No youth unemployment data found")

            if result.get('youth_unemployment_note'):
                note = result['youth_unemployment_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
