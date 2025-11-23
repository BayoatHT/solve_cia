import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_diplomatic_representation_from_us(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """Parse diplomatic representation from us from CIA Government section."""
    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        field_mappings = {
            'chief of mission': 'chief_of_mission',
            'embassy': 'embassy',
            'mailing address': 'mailing_address',
            'telephone': 'telephone',
            'FAX': 'fax',
            'email address and website': 'email_website',
            'consulate(s) general': 'consulates_general',
            'branch office(s)': 'branch_offices',
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
                result['diplomatic_representation_from_us_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing diplomatic_representation_from_us: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "FAX" -'diplomatic_rep_from_us_fax'
    # "branch office(s)" - 'diplomatic_rep_from_us_branch_offices'
    # "chief of mission" -  'diplomatic_rep_from_us_chief_of_mission'
    # "consulate(s)" - 'diplomatic_rep_from_us_consulates'
    # "consulate(s) general" -  'diplomatic_rep_from_us_consulates_general'
    # "email address and website" -  'diplomatic_rep_from_us_email'
    # "embassy" - 'diplomatic_rep_from_us_embassy'
    # "mailing address" - 'diplomatic_rep_from_us_mailing_address'
    # "note" - 'diplomatic_rep_from_us_note'
    # "other offices" - 'diplomatic_rep_from_us_other_offices'
    # "telephone" - 'diplomatic_rep_from_us_telephone'
    # --------------------------------------------------------------------------------------------------
    # ['diplomatic_rep_from_us_fax', 'diplomatic_rep_from_us_branch_offices', 'diplomatic_rep_from_us_chief_of_mission',
    # 'diplomatic_rep_from_us_consulates', 'diplomatic_rep_from_us_consulates_general', 'diplomatic_rep_from_us_email',
    # 'diplomatic_rep_from_us_embassy', 'diplomatic_rep_from_us_mailing_address', 'diplomatic_rep_from_us_note',
    # 'diplomatic_rep_from_us_other_offices', 'diplomatic_rep_from_us_telephone']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "chief of mission": {
            "text": "Ambassador Tulinabo S. MUSHINGI (since 9 March 2022)"
        },
        "embassy": {
            "text": "Rua Houari Boumedienne, #32, Luanda"
        },
        "mailing address": {
            "text": "2550 Luanda Place, Washington, DC 20521-2550"
        },
        "telephone": {
            "text": "[244] (222) 64-1000"
        },
        "FAX": {
            "text": "[244] (222) 64-1000"
        },
        "email address and website": {
            "text": "<br>Consularluanda@state.gov<br><br>https://ao.usembassy.gov/"
        }
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Diplomatic representation from the US'
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
    test_diplomatic_representation_from_us_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Diplomatic representation from the US Orginal Data")
    for index, country_data in enumerate(test_diplomatic_representation_from_us_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing diplomatic_representation_from_us Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_diplomatic_representation_from_us_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_diplomatic_representation_from_us(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
