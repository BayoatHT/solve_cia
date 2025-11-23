import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_legislative_branch(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """Parse legislative branch data from CIA Government section."""
    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        field_mappings = {
            'description': 'legislature_description',
            'elections': 'legislature_elections',
            'election results': 'legislature_election_results',
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
                result['legislative_branch_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing legislative branch: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "description" - 'legislative_branch_description',
    # "election results" - 'legislative_branch_election_results',
    # "elections" - 'legislative_branch_elections',
    # "note" - 'legislative_branch_note',
    # --------------------------------------------------------------------------------------------------
    # ['legislative_branch_description', 'legislative_branch_election_results',
    # 'legislative_branch_elections', 'legislative_branch_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "description": {
            "text": "bicameral Congress consists of:<br>Senate (100 seats; 2 members directly elected in each of the 50 state constituencies by simple majority vote except in Georgia and Louisiana which require an absolute majority vote with a second round if needed; members serve 6-year terms with one-third of membership renewed every 2 years)<br>House of Representatives (435 seats; members directly elected in single-seat constituencies by simple majority vote except in Georgia which requires an absolute majority vote with a second round if needed; members serve 2-year terms)"
        },
        "elections": {
            "text": "Senate - last held on 8 November 2022 (next to be held on 5 November 2024)<br>House of Representatives - last held on 8 November 2022 (next to be held on 5 November 2024)"
        },
        "election results": {
            "text": "Senate - percent of vote by party - NA; seats by party - Democratic Party 51, Republican Party 49; composition - men 75, women 25, percentage women 25%<br><br>House of Representatives - percent of vote by party - NA; seats by party - Republican Party 222, Democratic Party 213; composition - men 305, women 126, percentage women 29.2%; total US Congress percentage women 28.4%"
        },
        "note": "<strong>note:</strong> in addition to the regular members of the House of Representatives there are 6 non-voting delegates elected from the District of Columbia and the US territories of American Samoa, Guam, Puerto Rico, the Northern Mariana Islands, and the Virgin Islands; these are single seat constituencies directly elected by simple majority vote to serve a 2-year term (except for the resident commissioner of Puerto Rico who serves a 4-year term); the delegate can vote when serving on a committee and when the House meets as the Committee of the Whole House, but not when legislation is submitted for a “full floor” House vote; election of delegates last held on 8 November 2022 (next to be held on 3 November 2024)"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Legislative branch'
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
    test_legislative_branch_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Legislative branch Orginal Data")
    for index, country_data in enumerate(test_legislative_branch_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing legislative_branch Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_legislative_branch_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_legislative_branch(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
