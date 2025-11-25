import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_08_communications.helper.utils.parse_comms_value import parse_comms_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_broadband_fixed(iso3Code: str) -> dict:
    """Parse Broadband - fixed subscriptions from CIA Communications section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    comms_section = raw_data.get('Communications', {})
    pass_data = comms_section.get('Broadband - fixed subscriptions', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        field_mappings = {'total': 'broadband_total', 'subscriptions per 100 inhabitants': 'broadband_per_100'}
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in pass_data:
                field_data = pass_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        parsed = parse_comms_value(text)
                        if parsed['value'] is not None:
                            result[f'{output_prefix}_value'] = parsed['value']
                        if parsed['unit']:
                            result[f'{output_prefix}_unit'] = parsed['unit']
                        if parsed['year']:
                            result[f'{output_prefix}_year'] = parsed['year']
                        if parsed['is_estimate']:
                            result[f'{output_prefix}_is_estimate'] = parsed['is_estimate']
        if 'note' in pass_data:
            note_data = pass_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['broadband_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['broadband_note'] = clean_text(note_data)
    except Exception as e:
        logger.error(f"Error parsing parse_broadband_fixed for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_broadband_fixed")
    print("="*60)
    for iso3 in ['CHN', 'USA', 'JPN', 'DEU', 'GBR', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_broadband_fixed(iso3)
            if result:
                for key, val in result.items():
                    if key.endswith('_value'):
                        unit_key = key.replace('_value', '_unit')
                        unit = result.get(unit_key, '')
                        print(f"  {key}: {val:,.0f} {unit}")
                    elif not key.endswith(('_unit', '_year', '_is_estimate')):
                        print(f"  {key}: {val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
