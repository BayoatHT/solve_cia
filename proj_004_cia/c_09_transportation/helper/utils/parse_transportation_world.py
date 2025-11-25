import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_transportation_world(iso3Code: str) -> dict:
    """Parse World-level transportation data from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})

    if not transport_section or not isinstance(transport_section, dict):
        return result

    try:
        # For World data, parse all available fields
        for key, val in transport_section.items():
            if isinstance(val, dict) and 'text' in val:
                text = val['text']
                if text and isinstance(text, str):
                    clean_key = key.lower().replace(' ', '_').replace('-', '_')
                    result[clean_key] = clean_text(text)
            elif isinstance(val, str):
                clean_key = key.lower().replace(' ', '_').replace('-', '_')
                result[clean_key] = clean_text(val)

    except Exception as e:
        logger.error(f"Error parsing transportation_world for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_transportation_world")
    print("="*60)
    for iso3 in ['WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_transportation_world(iso3)
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
