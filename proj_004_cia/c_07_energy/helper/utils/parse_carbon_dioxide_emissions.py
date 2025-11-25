import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_carbon_dioxide_emissions(iso3Code: str) -> dict:
    """Parse carbon dioxide emissions from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    carbon_data = energy_section.get('Carbon dioxide emissions', {})

    if not carbon_data or not isinstance(carbon_data, dict):
        return result
    try:
        field_mappings = {
            'total emissions': 'carbon_total',
            'from coal and metallurgical coke': 'carbon_coal',
            'from petroleum and other liquids': 'carbon_petroleum',
            'from consumed natural gas': 'carbon_natural_gas',
        }
        for cia_key, output_prefix in field_mappings.items():
            if cia_key in carbon_data:
                field_data = carbon_data[cia_key]
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
        if 'note' in carbon_data:
            note_data = carbon_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note = note_data['text']
                if note and isinstance(note, str) and note.strip():
                    result['carbon_note'] = clean_text(note)
            elif isinstance(note_data, str) and note_data.strip():
                result['carbon_note'] = clean_text(note_data)
    except Exception as e:
        logger.error(f"Error parsing carbon_dioxide_emissions for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_carbon_dioxide_emissions")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'RUS', 'IND', 'DEU', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_carbon_dioxide_emissions(iso3)
            if result:
                total = result.get('carbon_total_value')
                coal = result.get('carbon_coal_value')
                petroleum = result.get('carbon_petroleum_value')
                gas = result.get('carbon_natural_gas_value')
                if total:
                    print(f"  Total: {total:,.0f} {result.get('carbon_total_unit', '')}")
                if coal:
                    print(f"  Coal: {coal:,.0f} {result.get('carbon_coal_unit', '')}")
                if petroleum:
                    print(f"  Petroleum: {petroleum:,.0f} {result.get('carbon_petroleum_unit', '')}")
                if gas:
                    print(f"  Natural gas: {gas:,.0f} {result.get('carbon_natural_gas_unit', '')}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
