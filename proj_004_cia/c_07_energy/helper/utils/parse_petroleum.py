import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_petroleum(iso3Code: str, return_original: bool = False)-> dict:
    """Parse Petroleum from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    pass_data = energy_section.get('Petroleum', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        field_mappings = {'total petroleum production': 'petrol_production', 'refined petroleum consumption': 'petrol_consumption', 'crude oil estimated reserves': 'petrol_reserves'}
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in pass_data:
                field_data = pass_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        parsed = parse_energy_value(text)
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
                    result['petroleum_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['petroleum_note'] = clean_text(note_data)
    except Exception as e:
        logger.error(f"Error parsing parse_petroleum for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_petroleum")
    print("="*60)
    for iso3 in ['USA', 'SAU', 'RUS', 'CAN', 'CHN', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_petroleum(iso3)
            if result:
                for key, val in result.items():
                    if key.endswith('_value'):
                        unit_key = key.replace('_value', '_unit')
                        unit = result.get(unit_key, '')
                        print(f"  {key}: {val:,.0f} {unit}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
