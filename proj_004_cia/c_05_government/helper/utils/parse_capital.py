import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_capital(iso3Code: str) -> dict:
    """Parse capital city data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Capital', {})

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
        logger.error(f"Error parsing capital for {iso3Code}: {e}")

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


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_capital")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'JPN']:
        print(f"\n{iso3}:")
        try:
            result = parse_capital(iso3)
            if result:
                print(f"  Name: {result.get('capital_name', 'N/A')}")
                print(f"  Coords: {result.get('capital_latitude', 'N/A')}, {result.get('capital_longitude', 'N/A')}")
                print(f"  UTC: {result.get('capital_utc_offset_hours', 'N/A')}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
