import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_executive_branch(
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
    # "cabinet" - 'executive_branch_cabinet'
    # "chief of state" - 'executive_branch_chief_of_state'
    # "election results" - 'executive_branch_election_results'
    # "elections/appointments" - 'executive_branch_elections'
    # "head of government" - 'executive_branch_head_of_government'
    # "note" - 'executive_branch_note'
    # "state counsellor" - 'executive_branch_state_counsellor'
    # --------------------------------------------------------------------------------------------------
    # ['executive_branch_cabinet', 'executive_branch_chief_of_state', 'executive_branch_election_results',
    # 'executive_branch_elections', 'executive_branch_head_of_government', 'executive_branch_note',
    # 'executive_branch_state_counsellor']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "chief of state": {
            "text": "President Joseph R. BIDEN, Jr. (since 20 January 2021)"
        },
        "head of government": {
            "text": "President Joseph R. BIDEN, Jr. (since 20 January 2021)"
        },
        "cabinet": {
            "text": "Cabinet appointed by the president, approved by the Senate"
        },
        "elections/appointments": {
            "text": "president and vice president indirectly elected on the same ballot by the Electoral College of 'electors' chosen from each state; president and vice president serve a 4-year term (eligible for a second term); election last held on 3 November 2020 (next to be held on 5 November 2024)"
        },
        "election results": {
            "text": "<em><br>2020:</em> Joseph R. BIDEN, Jr. elected president; electoral vote - Joseph R. BIDEN, Jr. (Democratic Party) 306, Donald J. TRUMP (Republican Party) 232; percent of direct popular vote - Joseph R. BIDEN Jr. 51.3%, Donald J. TRUMP 46.9%, other 1.8%<br><br><em>2016:</em> Donald J. TRUMP elected president; electoral vote - Donald J. TRUMP (Republican Party) 304, Hillary D. CLINTON (Democratic Party) 227, other 7; percent of direct popular vote - Hillary D. CLINTON 48.2%, Donald J. TRUMP 46.1%, other 5.7%"
        },
        "note": "<strong>note:</strong> the president is both chief of state and head of government"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Executive branch'
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
    test_executive_branch_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Executive branchs Orginal Data")
    for index, country_data in enumerate(test_executive_branch_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing executive_branch Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_executive_branch_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_executive_branch(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
