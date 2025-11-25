import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_ports_and_terminals(iso3Code: str) -> dict:
    """Parse ports and terminals from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    ports_data = transport_section.get('Ports and terminals', {})

    if not ports_data or not isinstance(ports_data, dict):
        return result

    try:
        # Parse each sub-field (e.g., major seaport(s), oil terminal(s), container port(s), etc.)
        for key, val in ports_data.items():
            if isinstance(val, dict) and 'text' in val:
                text = val['text']
                if text and isinstance(text, str):
                    # Create key like "ports_major_seaport"
                    clean_key = key.lower().replace(' ', '_').replace('(', '').replace(')', '')
                    result[f'ports_{clean_key}'] = clean_text(text)
            elif isinstance(val, str):
                clean_key = key.lower().replace(' ', '_').replace('(', '').replace(')', '')
                result[f'ports_{clean_key}'] = clean_text(val)

    except Exception as e:
        logger.error(f"Error parsing ports_and_terminals for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_ports_and_terminals")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'SGP', 'NLD', 'UAE', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_ports_and_terminals(iso3)
            if result:
                for key, val in result.items():
                    val_str = str(val)
                    print(f"  {key}: {val_str[:60] if len(val_str) > 60 else val_str}...")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
