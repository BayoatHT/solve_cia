import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_national_heritage(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """Parse national heritage from CIA Government section."""
    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        field_mappings = {
            'total World Heritage Sites': 'total_world_heritage_sites',
            'selected World Heritage Site locales': 'world_heritage_locales',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in test_data:
                field_data = test_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
                elif isinstance(field_data, str) and field_data.strip():
                    result[output_key] = clean_text(field_data)
        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['national_heritage_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing national_heritage: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'national_heritage_note',
    # "selected World Heritage Site locales" - 'national_heritage_selected_sites',
    # "total World Heritage Sites" - 'national_heritage_total_sites',
    # --------------------------------------------------------------------------------------------------
    # ['national_heritage_note', 'national_heritage_selected_sites', 'national_heritage_total_sites']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "total World Heritage Sites": {
            "text": "25 (12 cultural, 12 natural, 1 mixed); note - includes one site in Puerto Rico"
        },
        "selected World Heritage Site locales": {
            "text": "Yellowstone National Park (n); Grand Canyon National Park (n); Cahokia Mounds State Historic Site (c); Independence Hall (c); Statue of Liberty (c); Yosemite National Park (n); Papahānaumokuākea (m); Monumental Earthworks of Poverty Point (c); The 20th-Century Architecture of Frank Lloyd Wright (c); Mesa Verde National Park (c); Mammoth Cave National Park (n); Monticello (c); Olympic National Park (n)"
        }
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'National heritage'
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
    test_national_heritage_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test National heritage Orginal Data")
    for index, country_data in enumerate(test_national_heritage_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing national_heritage Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_national_heritage_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_national_heritage(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
