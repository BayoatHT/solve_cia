import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_country_name(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "abbreviation" - 'country_name_abbrev'
    # "conventional long form" - 'country_name_long_form'
    # "conventional short form" - 'country_name_short_form'
    # "etymology" - 'country_name_etymology'
    # "former" - 'country_name_former'
    # "local long form" - 'country_name_local_long_form'
    # "local short form" - 'country_name_local_short_form'
    # "note" - 'country_name_note'
    # "official long form" - 'country_name_official_long_form'
    # "official short form" - 'country_name_official_short_form'
    # --------------------------------------------------------------------------------------------------
    # ['country_name_abbrev', 'country_name_long_form', 'country_name_short_form', 'country_name_etymology',
    # 'country_name_former', 'country_name_local_long_form', 'country_name_local_short', 'country_name_note',
    # 'country_name_official_long_form', 'country_name_official_short_form']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "conventional long form": {
            "text": "United States of America"
        },
        "conventional short form": {
            "text": "United States"
        },
        "abbreviation": {
            "text": "US or USA"
        },
        "etymology": {
            "text": "the name America is derived from that of Amerigo VESPUCCI (1454-1512) - Italian explorer, navigator, and cartographer - using the Latin form of his name, Americus, feminized to America"
        },
        "note": ""
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Country name'
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
    test_country_name_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Country name Orginal Data")
    for index, country_data in enumerate(test_country_name_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing country_name Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_country_name_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_country_name(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
