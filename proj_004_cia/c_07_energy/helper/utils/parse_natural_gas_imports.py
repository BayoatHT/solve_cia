import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_natural_gas_imports(iso3Code: str) -> dict:
    """Parse Natural gas - imports from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    pass_data = energy_section.get('Natural gas - imports', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['nat_gas_imports_value'] = parsed['value']
                if parsed['unit']:
                    result['nat_gas_imports_unit'] = parsed['unit']
                if parsed['year']:
                    result['nat_gas_imports_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['nat_gas_imports_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logger.error(f"Error parsing parse_natural_gas_imports for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_natural_gas_imports")
    print("="*60)
    for iso3 in ['DEU', 'CHN', 'JPN', 'ITA', 'USA', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_natural_gas_imports(iso3)
            if result:
                value = result.get('nat_gas_imports_value')
                unit = result.get('nat_gas_imports_unit', '')
                year = result.get('nat_gas_imports_year', 'N/A')
                if value:
                    print(f"  Value: {value:,.0f} {unit} ({year})")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
