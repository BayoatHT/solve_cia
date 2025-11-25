import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_07_energy.helper.utils.parse_energy_value import parse_energy_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_carbon_dioxide_from_consumption(iso3Code: str, return_original: bool = False)-> dict:
    """Parse carbon dioxide from consumption of energy from CIA Energy section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    energy_section = raw_data.get('Energy', {})
    carbon_data = energy_section.get('Carbon dioxide emissions from consumption of energy', {})

    if return_original:
        return carbon_data


    if not carbon_data or not isinstance(carbon_data, dict):
        return result

    try:
        if 'text' in carbon_data:
            text = carbon_data['text']
            if text and isinstance(text, str):
                parsed = parse_energy_value(text)
                if parsed['value'] is not None:
                    result['co2_energy_value'] = parsed['value']
                if parsed['unit']:
                    result['co2_energy_unit'] = parsed['unit']
                if parsed['year']:
                    result['co2_energy_year'] = parsed['year']
                if parsed['is_estimate']:
                    result['co2_energy_is_estimate'] = parsed['is_estimate']
    except Exception as e:
        logger.error(f"Error parsing carbon_dioxide_from_consumption for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_carbon_dioxide_from_consumption")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'RUS', 'IND', 'DEU', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_carbon_dioxide_from_consumption(iso3)
            if result:
                value = result.get('co2_energy_value')
                unit = result.get('co2_energy_unit', '')
                year = result.get('co2_energy_year', 'N/A')
                if value:
                    print(f"  CO2 from energy: {value:,.0f} {unit} ({year})")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
