import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_national_anthem(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """Parse national anthem from CIA Government section."""
    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        field_mappings = {
            'name': 'anthem_name',
            'lyrics/music': 'anthem_lyrics_music',
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
                result['national_anthem_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing national_anthem: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "lyrics/music" - 'national_anthem_lyrics_music',
    # "name" - 'national_anthem_name',
    # "note" - 'national_anthem_note',
    # --------------------------------------------------------------------------------------------------
    # ['national_anthem_lyrics_music', 'national_anthem_name', 'national_anthem_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "name": {
            "text": "\"The Star-Spangled Banner\""
        },
        "lyrics/music": {
            "text": "Francis Scott KEY/John Stafford SMITH"
        },
        "note": "<strong>note:</strong> adopted 1931; during the War of 1812, after witnessing the successful American defense of Fort McHenry in Baltimore following British naval bombardment, Francis Scott KEY wrote the lyrics to what would become the national anthem; the lyrics were set to the tune of \"The Anacreontic Song\"; only the first verse is sung"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'National anthem'
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
    test_national_anthem_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test National anthem Orginal Data")
    for index, country_data in enumerate(test_national_anthem_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing national_anthem Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_national_anthem_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_national_anthem(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
