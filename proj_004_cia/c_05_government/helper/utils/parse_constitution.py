import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_constitution(
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
    # "amendments" - 'constitution_amendments'
    # "history" - 'constitution_history'
    # "note" - 'constitution_note'
    # --------------------------------------------------------------------------------------------------
    # ['constitution_amendments', 'constitution_history', 'constitution_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "history": {
            "text": "previous 1781 (Articles of Confederation and Perpetual Union); latest drafted July - September 1787, submitted to the Congress of the Confederation 20 September 1787, submitted for states' ratification 28 September 1787, ratification completed by nine of the 13 states 21 June 1788, effective 4 March 1789"
        },
        "amendments": {
            "text": "proposed as a \"joint resolution\" by Congress, which requires a two-thirds majority vote in both the House of Representatives and the Senate or by a constitutional convention called for by at least two thirds of the state legislatures; passage requires ratification by three fourths of the state legislatures or passage in state-held constitutional conventions as specified by Congress; the US president has no role in the constitutional amendment process; amended many times, last in 1992"
        },
        "note": ""
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Constitution'
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
    test_constitution_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test ConstitutionOrginal Data")
    for index, country_data in enumerate(test_constitution_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing constitution Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_constitution_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_constitution(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
