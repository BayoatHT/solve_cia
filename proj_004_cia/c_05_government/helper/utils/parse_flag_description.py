import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_flag_description(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parse flag description from CIA Government section.

    Args:
        test_data: Dictionary containing flag description data
        iso3Code: ISO3 country code

    Returns:
        Dictionary with parsed flag description
    """
    result = {}

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        # Extract main text
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['flag_description'] = clean_text(text)

                # Extract colors mentioned
                colors = _extract_flag_colors(text)
                if colors:
                    result['flag_colors'] = colors

        # Handle note
        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['flag_description_note'] = clean_text(note)

    except Exception as e:
        app_logger.error(f"Error parsing flag description: {e}")

    return result


def _extract_flag_colors(text: str) -> list:
    """Extract colors mentioned in flag description."""
    if not text:
        return []

    text_lower = text.lower()
    color_keywords = [
        'red', 'blue', 'green', 'yellow', 'white', 'black', 'orange',
        'gold', 'purple', 'brown', 'pink', 'cyan', 'maroon', 'navy',
        'scarlet', 'crimson', 'azure', 'cerulean', 'saffron'
    ]

    found_colors = []
    for color in color_keywords:
        if color in text_lower:
            found_colors.append(color)

    return found_colors


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'flag_description_note'
    # "text" - 'flag_description'
    # --------------------------------------------------------------------------------------------------
    # ['flag_description_note', 'flag_description']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "13 equal horizontal stripes of red (top and bottom) alternating with white; there is a blue rectangle in the upper hoist-side corner bearing 50 small, white, five-pointed stars arranged in nine offset horizontal rows of six stars (top and bottom) alternating with rows of five stars; the 50 stars represent the 50 states, the 13 stripes represent the 13 original colonies; blue stands for loyalty, devotion, truth, justice, and friendship, red symbolizes courage, zeal, and fervency, while white denotes purity and rectitude of conduct; commonly referred to by its nickname of Old Glory",
        "note": "<strong>note:</strong> the design and colors have been the basis for a number of other flags, including Chile, Liberia, Malaysia, and Puerto Rico"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Flag description'
    # --------------------------------------------------------------------------------------------------
    # List of countries to test
    test_countries = ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'IND'
                      'RUS', 'BRA', 'JPN', 'AUS', 'CAN', 'MEX'
                      'ZAF', 'KOR', 'ITA', 'ESP', 'NLD', 'SWE',
                      'NOR', 'FIN', 'DNK', 'POL', 'TUR', 'ARG',
                      'CHL', 'PER', 'COL', 'VEN', 'EGY', 'SAR',
                      'UAE', 'ISR', 'IRN', 'PAK', 'BGD', 'PHL',
                      'IDN', 'MYS', 'THA', 'VNM', 'SGP', 'NZL',
                      'KHM', 'MMR', 'LKA', 'NPL', 'BTN', 'MDV',
                      'KAZ', 'UZB', 'TKM', 'KGZ', 'TJK', 'AZE',
                      'GEO', 'ARM', 'MDA', 'UKR', 'BLR', 'LVA',]
    # --------------------------------------------------------------------------------------------------
    test_flag_description_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Flag description Orginal Data")
    for index, country_data in enumerate(test_flag_description_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing flag_description Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_flag_description_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_flag_description(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
