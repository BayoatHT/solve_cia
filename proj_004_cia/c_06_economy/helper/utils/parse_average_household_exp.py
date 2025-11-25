import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_average_household_exp(iso3Code: str) -> dict:
    """
    Parse average household expenditures data from CIA World Factbook for a given country.

    This parser extracts household expenditure information including:
    - Percentage spent on food
    - Percentage spent on alcohol and tobacco
    - Year of data

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN', 'WLD')

    Returns:
        Dictionary with structured household expenditure data:
        {
            "avg_house_expend_food": {"value": float, "unit": str, "date": str},
            "avg_house_expend_alcohol_tobacco": {"value": float, "unit": str, "date": str}
        }

    Examples:
        >>> data = parse_average_household_exp('USA')
        >>> 'avg_house_expend_food' in data
        True

        >>> data = parse_average_household_exp('CHN')
        >>> data.get('avg_house_expend_food', {}).get('value') > 0
        True
    """
    result = {}

    # Load raw country data
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    # Navigate to Economy -> Average household expenditures
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Average household expenditures', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        # Define mapping for keys
        expenditure_keys = {
            "on food": "avg_house_expend_food",
            "on alcohol and tobacco": "avg_house_expend_alcohol_tobacco"
        }

        for key, result_key in expenditure_keys.items():
            item = pass_data.get(key, {}).get("text", "")

            # Define default values for result
            result[result_key] = {"value": 0, "unit": "%", "date": ""}

            # Match the pattern for value, unit, and date
            match = re.match(
                r"([\d.]+)% of household expenditures \((\d{4}) est\.\)", item)

            if match:
                result[result_key]["value"] = float(match.group(1))
                result[result_key]["date"] = match.group(2)

    except Exception as e:
        logger.error(f"Error parsing average_household_exp for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    """Test parse_average_household_exp with real country data."""
    print("="*60)
    print("Testing parse_average_household_exp across countries")
    print("="*60)

    test_countries = ['USA', 'CHN', 'IND', 'DEU', 'JPN', 'WLD']

    for iso3 in test_countries:
        print(f"\n{iso3}:")
        try:
            result = parse_average_household_exp(iso3)

            if result.get('avg_house_expend_food'):
                food = result['avg_house_expend_food']
                if food.get('value') > 0:
                    print(f"  Food: {food['value']}% ({food['date']})")

            if result.get('avg_house_expend_alcohol_tobacco'):
                alcohol = result['avg_house_expend_alcohol_tobacco']
                if alcohol.get('value') > 0:
                    print(f"  Alcohol/Tobacco: {alcohol['value']}% ({alcohol['date']})")

            if (not result.get('avg_house_expend_food') or result.get('avg_house_expend_food', {}).get('value', 0) == 0):
                print("  No household expenditure data found")

        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")

    print("\n" + "="*60)
    print("✓ Tests complete")
