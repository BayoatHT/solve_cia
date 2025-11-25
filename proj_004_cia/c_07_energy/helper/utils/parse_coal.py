import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_coal(iso3Code: str) -> dict:
    """Parse coal data from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    coal_data = energy_section.get('Coal', {})

    if not coal_data or not isinstance(coal_data, dict):
        return result

    try:
        field_mappings = {
            'production': 'coal_production',
            'consumption': 'coal_consumption',
            'exports': 'coal_exports',
            'imports': 'coal_imports',
            'proven reserves': 'coal_reserves'
        }
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in coal_data:
                field_data = coal_data[cia_key]
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
        if 'note' in coal_data:
            note_data = coal_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['coal_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['coal_note'] = clean_text(note_data)
    except Exception as e:
        logger.error(f"Error parsing coal for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_coal")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'RUS', 'AUS', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_coal(iso3)
            if result:
                prod = result.get('coal_production_value')
                cons = result.get('coal_consumption_value')
                if prod:
                    print(f"  Production: {prod:,.0f} {result.get('coal_production_unit', '')}")
                if cons:
                    print(f"  Consumption: {cons:,.0f} {result.get('coal_consumption_unit', '')}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
