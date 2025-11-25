import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_credit_ratings(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse credit ratings data from CIA World Factbook for a given country.

    This parser extracts credit ratings information including:
    - Fitch rating and year
    - Moody's rating and year
    - Standard & Poor's rating and year
    - Related notes

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured credit ratings data:
        {
            "credit_fitch_rating": {"rating": str, "year": int},
            "credit_moodys_rating": {"rating": str, "year": int},
            "credit_standard_poor_rating": {"rating": str, "year": int},
            "credit_ratings_note": str
        }

    Examples:
        >>> data = parse_credit_ratings('USA')
        >>> 'credit_fitch_rating' in data
        True

        >>> data = parse_credit_ratings('DEU')
        >>> data.get('credit_moodys_rating', {}).get('rating') is not None
        True
    """
    result = {
        "credit_ratings_note": "",
        "credit_fitch_rating": {},
        "credit_moodys_rating": {},
        "credit_standard_poor_rating": {}
    }

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Credit ratings
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Credit ratings', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Parse the note if present
        result["credit_ratings_note"] = clean_text(pass_data.get("note", ""))

        # Helper function to parse rating and year from text
        def parse_rating(text: str, return_original: bool = False)-> dict:
            if return_original:
                return text

            match = re.match(r"([A-Za-z+]+)\s*\((\d{4})\)", text)
            if match:
                return {
                    "rating": match.group(1),
                    "year": int(match.group(2))
                }
            return {"rating": "", "year": 0}

        # Parse each rating if present
        if "Fitch rating" in pass_data:
            result["credit_fitch_rating"] = parse_rating(
                pass_data["Fitch rating"].get("text", ""))
        if "Moody's rating" in pass_data:
            result["credit_moodys_rating"] = parse_rating(
                pass_data["Moody's rating"].get("text", ""))
        if "Standard & Poors rating" in pass_data:
            result["credit_standard_poor_rating"] = parse_rating(
                pass_data["Standard & Poors rating"].get("text", ""))

    except Exception as e:
        logger.error(f"Error parsing credit_ratings for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_credit_ratings with real country data."""
    print("="*60)
    print("Testing parse_credit_ratings across countries")
    print("="*60)

    test_countries = ['USA', 'DEU', 'FRA', 'GBR', 'JPN', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_credit_ratings(iso3)

            if result.get('credit_fitch_rating', {}).get('rating'):
                fitch = result['credit_fitch_rating']
                print(f"  Fitch: {fitch['rating']} ({fitch['year']})")

            if result.get('credit_moodys_rating', {}).get('rating'):
                moodys = result['credit_moodys_rating']
                print(f"  Moody's: {moodys['rating']} ({moodys['year']})")

            if result.get('credit_standard_poor_rating', {}).get('rating'):
                sp = result['credit_standard_poor_rating']
                print(f"  S&P: {sp['rating']} ({sp['year']})")

            if not any([result.get('credit_fitch_rating', {}).get('rating'),
                       result.get('credit_moodys_rating', {}).get('rating'),
                       result.get('credit_standard_poor_rating', {}).get('rating')]):
                print("  No credit ratings data found")

            if result.get('credit_ratings_note'):
                note = result['credit_ratings_note'][:60]
                print(f"  Note: {note}...")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
