import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_ports(iso3Code: str, return_original: bool = False)-> dict:
    """Parse ports from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    ports_data = transport_section.get('Ports', {})

    if return_original:
        return ports_data


    if not ports_data:
        return result

    try:
        field_mappings = {
            'total ports': 'ports_total',
            'large': 'ports_large',
            'medium': 'ports_medium',
            'small': 'ports_small',
            'very small': 'ports_very_small',
            'ports with oil terminals': 'ports_oil_terminals',
            'size unknown': 'ports_size_unknown',
        }

        for cia_field, output_prefix in field_mappings.items():
            if cia_field in ports_data:
                field_data = ports_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    parsed = parse_transport_value(field_data['text'])
                    if parsed['value'] is not None:
                        result[f'{output_prefix}_value'] = int(parsed['value'])
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']

        # Parse key ports list
        if 'key ports' in ports_data:
            key_ports_data = ports_data['key ports']
            if isinstance(key_ports_data, dict) and 'text' in key_ports_data:
                text = key_ports_data['text']
                ports_list = [clean_text(p.strip()) for p in text.split(',') if p.strip()]
                if ports_list:
                    result['ports_key_list'] = ports_list

    except Exception as e:
        logger.error(f"Error parsing ports for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_ports")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'JPN', 'SGP', 'NLD', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_ports(iso3)
            if result:
                for key, val in result.items():
                    if isinstance(val, list):
                        print(f"  {key}: {len(val)} ports")
                    else:
                        print(f"  {key}: {val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
