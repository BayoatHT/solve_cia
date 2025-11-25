import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_economic_overview(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """

    """
    if return_original:
        return test_data

    result = ""

    # Clean the text value and store it in the result dictionary
    result = clean_text(test_data.get("text", ""))

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 10 >>> 'Economic overview'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'economic_overview_note'
    # "text" - 'economic_overview'
    # --------------------------------------------------------------------------------------------------
    # ['economic_overview', 'economic_overview_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "Western Sahara has a small market-based economy whose main industries are fishing, phosphate mining, tourism, and pastoral nomadism. The territory's arid desert climate makes sedentary agriculture difficult, and much of its food is imported. The Moroccan Government administers Western Sahara's economy and is a key source of employment, infrastructure development, and social spending in the territory. ++ Western Sahara's unresolved legal status makes the exploitation of its natural resources a contentious issue between Morocco and the Polisario. Morocco and the EU in December 2013 finalized a four-year agreement allowing European vessels to fish off the coast of Morocco, including disputed waters off the coast of Western Sahara. As of April 2018, Moroccan and EU authorities were negotiating an amendment to renew the agreement. ++ Oil has never been found in Western Sahara in commercially significant quantities, but Morocco and the Polisario have quarreled over rights to authorize and benefit from oil exploration in the territory. Western Sahara's main long-term economic challenge is the development of a more diverse set of industries capable of providing greater employment and income to the territory. However, following King MOHAMMED VI's November 2015 visit to Western Sahara, the Government of Morocco announced a series of investments aimed at spurring economic activity in the region, while the General Confederation of Moroccan Enterprises announced a $609 million investment initiative in the region in March 2015."
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Capital'
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
    test_capital_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Admin Divisions Orginal Data")
    for index, country_data in enumerate(test_capital_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing Capital Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_capital_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_capital(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
