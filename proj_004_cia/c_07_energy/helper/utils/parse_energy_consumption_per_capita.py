import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_energy_consumption_per_capita(iso3Code: str) -> dict:
    """Parse energy consumption per capita from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    capita_section = energy_section.get('Energy consumption per capita', {})

    if not capita_section or not isinstance(capita_section, dict):
        return result

    try:
        # Find the first key that contains "Total energy consumption per capita"
        for key, value in capita_section.items():
            if 'Total energy consumption per capita' in key:
                if isinstance(value, dict) and 'text' in value:
                    text = value['text']
                    if text and isinstance(text, str):
                        parsed = parse_energy_value(text)
                        if parsed['value'] is not None:
                            result['energy_per_capita_value'] = parsed['value']
                        if parsed['unit']:
                            result['energy_per_capita_unit'] = parsed['unit']
                        if parsed['year']:
                            result['energy_per_capita_year'] = parsed['year']
                        if parsed['is_estimate']:
                            result['energy_per_capita_is_estimate'] = parsed['is_estimate']
                break
    except Exception as e:
        logger.error(f"Error parsing parse_energy_consumption_per_capita for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_energy_consumption_per_capita")
    print("="*60)
    for iso3 in ['USA', 'CAN', 'QAT', 'NOR', 'AUS', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_energy_consumption_per_capita(iso3)
            if result:
                value = result.get('energy_per_capita_value')
                unit = result.get('energy_per_capita_unit', '')
                year = result.get('energy_per_capita_year', 'N/A')
                if value:
                    print(f"  Value: {value:,.0f} {unit} ({year})")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
