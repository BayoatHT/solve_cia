import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_tele_systems(iso3Code: str) -> dict:
    """Parse Telecommunication systems from CIA Communications section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    comms_section = raw_data.get('Communications', {})
    pass_data = comms_section.get('Telecommunication systems', {})

    if not pass_data or not isinstance(pass_data, dict):
        return result

    try:
        if 'text' in pass_data:
            text = pass_data['text']
            if text and isinstance(text, str):
                result['tele_systems'] = clean_text(text)
    except Exception as e:
        logger.error(f"Error parsing parse_tele_systems for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_tele_systems")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_tele_systems(iso3)
            if result:
                for key, val in result.items():
                    print(f"  {key}: {val[:80] if isinstance(val, str) and len(val) > 80 else val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
