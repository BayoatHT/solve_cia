import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_major_aquifers(iso3Code: str) -> dict:
    """Parse major aquifers from CIA Environment section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    aquifer_data = environment_section.get('Major aquifers', {})

    if not aquifer_data:
        return result

    result = {
        "major_aquifers": {
            "aquifers": [],
            "raw_text": None
        },
        "major_aquifers_note": ""
    }

    text = aquifer_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['major_aquifers']['raw_text'] = cleaned

        # Split by comma or semicolon
        parts = re.split(r'[,;]', cleaned)
        for part in parts:
            part = part.strip()
            if part and len(part) > 2:
                result['major_aquifers']['aquifers'].append(part)

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_major_aquifers")
    print("="*60)
    for iso3 in ['USA', 'BRA', 'CHN', 'IND', 'SAU']:
        print(f"\n{iso3}:")
        try:
            result = parse_major_aquifers(iso3)
            if result:
                aquifers = result.get('major_aquifers', {}).get('aquifers', [])
                print(f"  Found {len(aquifers)} aquifers")
                for aq in aquifers[:3]:
                    print(f"    - {aq}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
