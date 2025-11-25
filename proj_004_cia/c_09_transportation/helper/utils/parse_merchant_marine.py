import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_merchant_marine(iso3Code: str) -> dict:
    """Parse merchant marine from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    merchant_marine_data = transport_section.get('Merchant marine', {})

    if not merchant_marine_data:
        return result

    try:
        # Parse total
        if 'total' in merchant_marine_data:
            total_data = merchant_marine_data['total']
            if isinstance(total_data, dict) and 'text' in total_data:
                parsed = parse_transport_value(total_data['text'])
                if parsed['value'] is not None:
                    result['merchant_total_value'] = int(parsed['value'])
                if parsed['year']:
                    result['merchant_total_year'] = parsed['year']

        # Parse by type
        if 'by type' in merchant_marine_data:
            by_type_data = merchant_marine_data['by type']
            if isinstance(by_type_data, dict) and 'text' in by_type_data:
                text = by_type_data['text']
                ship_types = []

                # Pattern: "bulk carrier 4, container ship 60, general cargo 96"
                segments = text.split(',')
                for segment in segments:
                    segment = segment.strip()
                    # Match pattern: "type name count"
                    match = re.match(r'(.+?)\s+(\d+)$', segment)
                    if match:
                        ship_type = match.group(1).strip()
                        count = int(match.group(2))
                        ship_types.append({'type': ship_type, 'count': count})

                if ship_types:
                    result['merchant_by_type'] = ship_types

        # Parse note
        if 'note' in merchant_marine_data:
            note = merchant_marine_data['note']
            if note and isinstance(note, str) and note.strip():
                result['merchant_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing merchant_marine for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_merchant_marine")
    print("="*60)
    for iso3 in ['CHN', 'JPN', 'GRC', 'USA', 'SGP', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_merchant_marine(iso3)
            if result:
                for key, val in result.items():
                    if isinstance(val, list):
                        print(f"  {key}: {len(val)} types")
                    else:
                        print(f"  {key}: {val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
