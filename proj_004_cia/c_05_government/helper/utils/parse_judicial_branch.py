import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_judicial_branch(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """Parse judicial branch data from CIA Government section."""
    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        field_mappings = {
            'highest court(s)': 'highest_courts',
            'highest courts': 'highest_courts',
            'judge selection and term of office': 'judge_selection',
            'subordinate courts': 'subordinate_courts',
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
                result['judicial_branch_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing judicial branch: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "highest court(s)" - 'judicial_branch_highest_court'
    # "judge selection and term of office" - 'judicial_branch_judge_selection'
    # "note" - 'judicial_branch_note'
    # "subordinate courts" - 'judicial_branch_subordinate_courts'
    # --------------------------------------------------------------------------------------------------
    # ['judicial_branch_highest_court', 'judicial_branch_judge_selection', 'judicial_branch_note','judicial_branch_subordinate_courts']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "highest court(s)": {
            "text": "US Supreme Court (consists of 9 justices - the chief justice and 8 associate justices)"
        },
        "judge selection and term of office": {
            "text": "president nominates and, with the advice and consent of the Senate, appoints Supreme Court justices; justices serve for life"
        },
        "subordinate courts": {
            "text": "Courts of Appeal (includes the US Court of Appeal for the Federal District and 12 regional appeals courts); 94 federal district courts in 50 states and territories"
        },
        "note": "<strong>note:</strong> the US court system consists of the federal court system and the state court systems; although each court system is responsible for hearing certain types of cases, neither is completely independent of the other, and the systems often interact"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Judicial branch'
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
    test_judicial_branch_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Judicial branch Orginal Data")
    for index, country_data in enumerate(test_judicial_branch_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing judicial_branch Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_judicial_branch_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_judicial_branch(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
