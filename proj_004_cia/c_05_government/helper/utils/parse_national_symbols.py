import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_national_symbols(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """Parse national symbols from CIA Government section."""
    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        # Handle simple text field
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['national_symbols'] = clean_text(text)
                # Try to extract colors from text
                colors = _extract_colors(text)
                if colors:
                    result['national_colors'] = colors

        # Handle nested fields (some entries have these)
        field_mappings = {
            'national symbol(s)': 'national_symbols',
            'national colors': 'national_colors',
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
                result['national_symbols_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing national_symbols: {e}")
    return result


def _extract_colors(text: str) -> list:
    """Extract national colors from text."""
    if not text:
        return []

    # Look for pattern like "national colors: red, white, blue"
    color_match = re.search(r'national colors?:?\s*([^;]+)', text.lower())
    if color_match:
        colors_text = color_match.group(1)
        colors = [c.strip() for c in colors_text.split(',')]
        return [c for c in colors if c and len(c) < 20]
    return []


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'national_symbols',
    # --------------------------------------------------------------------------------------------------
    # ['national_symbols']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "bald eagle; national colors: red, white, blue"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'National symbol(s)'
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
    test_national_symbols_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test National symbol(s) Orginal Data")
    for index, country_data in enumerate(test_national_symbols_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing national_symbols Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_national_symbols_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_national_symbols(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
