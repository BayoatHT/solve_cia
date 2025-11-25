import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_airports_paved(iso3Code: str, return_original: bool = False)-> dict:
    """Parse airports with paved runways from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    airports_paved_data = transport_section.get('Airports - with paved runways', {})

    if return_original:
        return airports_paved_data


    if not airports_paved_data:
        return result

    try:
        # Parse total
        if 'total' in airports_paved_data:
            total_data = airports_paved_data['total']
            if isinstance(total_data, dict) and 'text' in total_data:
                parsed = parse_transport_value(total_data['text'])
                if parsed['value'] is not None:
                    result['paved_runways_total_value'] = int(parsed['value'])
                if parsed['year']:
                    result['paved_runways_total_year'] = parsed['year']

        # Parse runway lengths
        by_length = []
        for key, val in airports_paved_data.items():
            if key == 'total':
                continue
            if isinstance(val, dict) and 'text' in val:
                parsed = parse_transport_value(val['text'])
                if parsed['value'] is not None:
                    by_length.append({
                        'range': key,
                        'count': int(parsed['value'])
                    })

        if by_length:
            result['paved_runways_by_length'] = by_length

    except Exception as e:
        logger.error(f"Error parsing airports_paved for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_airports_paved")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_airports_paved(iso3)
            if result:
                for key, val in result.items():
                    print(f"  {key}: {val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
