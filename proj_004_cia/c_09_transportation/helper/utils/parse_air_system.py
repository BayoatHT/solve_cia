import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_air_system(iso3Code: str) -> dict:
    """Parse national air transport system from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    air_system_data = transport_section.get('National air transport system', {})

    if not air_system_data:
        return result

    try:
        field_mappings = {
            'number of registered air carriers': 'air_carriers',
            'inventory of registered aircraft operated by air carriers': 'air_aircraft',
            'annual passenger traffic on registered air carriers': 'air_passengers',
            'annual freight traffic on registered air carriers': 'air_freight',
        }

        for cia_field, output_prefix in field_mappings.items():
            if cia_field in air_system_data:
                field_data = air_system_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    parsed = parse_transport_value(text)

                    if parsed['value'] is not None:
                        # For carriers and aircraft, use int; for passengers/freight, use float
                        if output_prefix in ['air_carriers', 'air_aircraft']:
                            result[f'{output_prefix}_value'] = int(parsed['value'])
                        else:
                            result[f'{output_prefix}_value'] = parsed['value']

                    if parsed['unit']:
                        result[f'{output_prefix}_unit'] = parsed['unit']
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']
                    if parsed['magnitude']:
                        result[f'{output_prefix}_magnitude'] = parsed['magnitude']

    except Exception as e:
        logger.error(f"Error parsing air_system for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_air_system")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'UAE', 'GBR', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_air_system(iso3)
            if result:
                for key, val in result.items():
                    if isinstance(val, float):
                        print(f"  {key}: {val:,.0f}")
                    else:
                        print(f"  {key}: {val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
