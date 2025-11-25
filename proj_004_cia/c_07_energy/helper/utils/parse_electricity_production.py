import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_electricity_production(iso3Code: str, return_original: bool = False)-> dict:
    """Parse electricity production from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    pass_data = energy_section.get('Electricity - production', {})

    if return_original:
        return pass_data


    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['elec_production_value'] = parsed['value']
                if parsed['unit']:
                    result['elec_production_unit'] = parsed['unit']
                if parsed['year']:
                    result['elec_production_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['elec_production_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logger.error(f"Error parsing parse_electricity_production for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_electricity_production")
    print("="*60)
    for iso3 in ['CHN', 'USA', 'IND', 'RUS', 'JPN', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_electricity_production(iso3)
            if result:
                value = result.get('elec_production_value')
                unit = result.get('elec_production_unit', '')
                year = result.get('elec_production_year', 'N/A')
                if value:
                    print(f"  Value: {value:,.0f} {unit} ({year})")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
