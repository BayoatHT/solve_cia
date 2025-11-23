import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_suffrage(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parse suffrage data from CIA Government section.

    Args:
        test_data: Dictionary containing suffrage data
        iso3Code: ISO3 country code

    Returns:
        Dictionary with parsed suffrage information
    """
    result = {}

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['suffrage_description'] = clean_text(text)

                # Try to extract voting age
                age_match = re.search(r'(\d{1,2})\s*years?\s*of\s*age', text.lower())
                if age_match:
                    result['voting_age'] = int(age_match.group(1))

                # Check if universal
                if 'universal' in text.lower():
                    result['universal_suffrage'] = True
                if 'compulsory' in text.lower():
                    result['compulsory_voting'] = True

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['suffrage_note'] = clean_text(note)

    except Exception as e:
        app_logger.error(f"Error parsing suffrage: {e}")

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'suffrage_note',
    # "text" - 'suffrage',
    # --------------------------------------------------------------------------------------------------
    # ['suffrage_note', 'suffrage']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "18 years of age; universal",
        "note": ""
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Suffrage'
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
    test_suffrage_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Suffarage Orginal Data")
    for index, country_data in enumerate(test_suffrage_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing suffrage Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_suffrage_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_suffrage(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
