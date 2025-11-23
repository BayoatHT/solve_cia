import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_food_insecurity(food_data: dict, iso3Code: str = None) -> dict:
    """Parse food insecurity data."""
    result = {
        "food_insecurity": {
            "exceptional_shortfall": None,
            "severe_localized": None,
            "widespread_lack_access": None,
            "has_food_insecurity": False
        },
        "food_insecurity_note": ""
    }

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
    test_data = {
        "severe localized food insecurity": {"text": "Due to conflict in region X, millions are affected"}
    }
    print(parse_food_insecurity(test_data))
