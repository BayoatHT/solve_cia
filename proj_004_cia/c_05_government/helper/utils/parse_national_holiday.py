import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_national_holiday(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parse national holiday data from CIA Government section.

    Args:
        test_data: Dictionary containing national holiday data
        iso3Code: ISO3 country code

    Returns:
        Dictionary with parsed national holiday information
    """
    result = {}

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['national_holiday_description'] = clean_text(text)

                # Try to extract date pattern (e.g., "4 July", "14 July")
                date_match = re.search(r'(\d{1,2}\s+\w+)', text)
                if date_match:
                    result['national_holiday_date'] = date_match.group(1)

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['national_holiday_note'] = clean_text(note)

    except Exception as e:
        app_logger.error(f"Error parsing national holiday: {e}")

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'national_holiday_note',
    # "text" - 'national_holiday',
    # --------------------------------------------------------------------------------------------------
    # ['national_holiday_note', 'national_holiday']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "Independence Day, 4 July (1776)"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'National holiday'
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
    test_national_holiday_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test National holiday Orginal Data")
    for index, country_data in enumerate(test_national_holiday_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing national_holiday Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_national_holiday_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_national_holiday(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
