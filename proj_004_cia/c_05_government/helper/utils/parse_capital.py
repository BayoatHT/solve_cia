import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_capital(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parse capital city data from CIA Government section.

    Extracts name, coordinates, time zone, daylight saving time, etymology.

    Args:
        test_data: Dictionary containing capital data
        iso3Code: ISO3 country code

    Returns:
        Dictionary with parsed capital fields
    """
    result = {}

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        # Field mappings: CIA key -> output key
        field_mappings = {
            'name': 'capital_name',
            'geographic coordinates': 'capital_coordinates',
            'time difference': 'capital_time_difference',
            'daylight saving time': 'capital_daylight_saving_time',
            'time zone note': 'capital_time_zone_note',
            'etymology': 'capital_etymology',
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

        # Handle note field
        if 'note' in test_data:
            note_data = test_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note_text = note_data['text']
            elif isinstance(note_data, str):
                note_text = note_data
            else:
                note_text = None

            if note_text and note_text.strip():
                result['capital_note'] = clean_text(note_text)

        # Parse coordinates if present
        if 'capital_coordinates' in result:
            coords = _parse_coordinates(result['capital_coordinates'])
            if coords:
                result['capital_latitude'] = coords.get('latitude')
                result['capital_longitude'] = coords.get('longitude')

        # Parse time difference to numeric
        if 'capital_time_difference' in result:
            utc_offset = _parse_utc_offset(result['capital_time_difference'])
            if utc_offset is not None:
                result['capital_utc_offset_hours'] = utc_offset

    except Exception as e:
        app_logger.error(f"Error parsing capital: {e}")

    return result


def _parse_coordinates(coord_text: str) -> dict:
    """Parse geographic coordinates like '38 53 N, 77 02 W'."""
    if not coord_text:
        return {}

    # Pattern: degrees minutes direction
    pattern = r'(\d+)\s+(\d+)\s*([NS]),?\s*(\d+)\s+(\d+)\s*([EW])'
    match = re.search(pattern, coord_text)

    if match:
        lat_deg, lat_min, lat_dir = int(match.group(1)), int(match.group(2)), match.group(3)
        lon_deg, lon_min, lon_dir = int(match.group(4)), int(match.group(5)), match.group(6)

        latitude = lat_deg + lat_min / 60
        longitude = lon_deg + lon_min / 60

        if lat_dir == 'S':
            latitude = -latitude
        if lon_dir == 'W':
            longitude = -longitude

        return {'latitude': round(latitude, 4), 'longitude': round(longitude, 4)}

    return {}


def _parse_utc_offset(time_text: str) -> float:
    """Parse UTC offset like 'UTC-5' or 'UTC+5.5'."""
    if not time_text:
        return None

    pattern = r'UTC([+-]?\d+(?:\.\d+)?)'
    match = re.search(pattern, time_text)

    if match:
        return float(match.group(1))

    return None


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "daylight saving time" - 'capital_daylight_saving_time'
    # "etymology" - 'capital_etymology'
    # "geographic coordinates" - 'capital_geo_coord'
    # "name" - 'capital_name'
    # "note" - 'capital_note'
    # "time difference" - 'capital_time_diff'
    # "time zone note" - 'capital_time_zone_note'
    # --------------------------------------------------------------------------------------------------
    # ['capital_daylight_saving_time', 'capital_etymology', 'capital_geo_coord',
    # 'capital_name', 'capital_note', 'capital_time_diff', 'capital_time_zone_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "name": {
            "text": "Washington, DC"
        },
        "geographic coordinates": {
            "text": "38 53 N, 77 02 W"
        },
        "time difference": {
            "text": "UTC-5 (during Standard Time)"
        },
        "daylight saving time": {
            "text": "+1hr, begins second Sunday in March; ends first Sunday in November"
        },
        "time zone note": {
            "text": "the 50 United States cover six time zones"
        },
        "etymology": {
            "text": "named after George WASHINGTON (1732-1799), the first president of the United States"
        }
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
