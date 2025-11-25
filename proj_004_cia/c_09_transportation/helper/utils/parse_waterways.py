import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_waterways(iso3Code: str) -> dict:
    """Parse Waterways from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    pass_data = transport_section.get('Waterways', {})

    if not pass_data:
        return result

    try:
        field_mappings = {}
        for cia_field, output_prefix in field_mappings.items():
            if cia_field in pass_data:
                field_data = pass_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    parsed = parse_transport_value(text)

                    if parsed['value'] is not None:
                        result[f'{output_prefix}_value'] = parsed['value']
                    if parsed['unit']:
                        result[f'{output_prefix}_unit'] = parsed['unit']
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']

        # Parse note
        if 'note' in pass_data:
            note = pass_data['note']
            if note and isinstance(note, str) and note.strip():
                result['waterways_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing parse_waterways for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_waterways")
    print("="*60)
    for iso3 in ['CHN', 'RUS', 'BRA', 'USA', 'IND', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_waterways(iso3)
            if result:
                for key, val in result.items():
                    if key.endswith('_value'):
                        unit_key = key.replace('_value', '_unit')
                        unit = result.get(unit_key, '')
                        print(f"  {key}: {val:,.0f} {unit}")
                    elif not key.endswith(('_unit', '_year', '_is_estimate')):
                        val_str = str(val)
                        print(f"  {key}: {val_str[:80] if len(val_str) > 80 else val_str}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
