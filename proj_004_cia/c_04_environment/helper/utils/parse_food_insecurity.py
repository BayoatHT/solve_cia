import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_food_insecurity(iso3Code: str) -> dict:
    """Parse food insecurity from CIA Environment section for a given country."""
    result = {
        "food_insecurity": {
            "exceptional_shortfall": None,
            "severe_localized": None,
            "widespread_lack_access": None,
            "has_food_insecurity": False
        },
        "food_insecurity_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    food_data = environment_section.get('Food insecurity', {})

    if not food_data or not isinstance(food_data, dict):
        return result

    # Check for exceptional shortfall
    exceptional = food_data.get('exceptional shortfall in aggregate food production/supplies', {})
    if exceptional and isinstance(exceptional, dict):
        text = exceptional.get('text', '')
        if text and text.upper() != 'NA':
            result['food_insecurity']['exceptional_shortfall'] = clean_text(text)
            result['food_insecurity']['has_food_insecurity'] = True

    # Check for severe localized
    severe = food_data.get('severe localized food insecurity', {})
    if severe and isinstance(severe, dict):
        text = severe.get('text', '')
        if text and text.upper() != 'NA':
            result['food_insecurity']['severe_localized'] = clean_text(text)
            result['food_insecurity']['has_food_insecurity'] = True

    # Check for widespread lack of access
    widespread = food_data.get('widespread lack of access', {})
    if widespread and isinstance(widespread, dict):
        text = widespread.get('text', '')
        if text and text.upper() != 'NA':
            result['food_insecurity']['widespread_lack_access'] = clean_text(text)
            result['food_insecurity']['has_food_insecurity'] = True

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_food_insecurity")
    print("="*60)
    # Food insecurity is rare - test African countries where it's more common
    for iso3 in ['ETH', 'SOM', 'SDN', 'YEM', 'AFG', 'USA']:
        print(f"\n{iso3}:")
        try:
            result = parse_food_insecurity(iso3)
            if result and result['food_insecurity']['has_food_insecurity']:
                fi = result['food_insecurity']
                if fi['exceptional_shortfall']:
                    print(f"  Exceptional: {fi['exceptional_shortfall'][:60]}...")
                if fi['severe_localized']:
                    print(f"  Severe: {fi['severe_localized'][:60]}...")
                if fi['widespread_lack_access']:
                    print(f"  Widespread: {fi['widespread_lack_access'][:60]}...")
            else:
                print("  No food insecurity data")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
