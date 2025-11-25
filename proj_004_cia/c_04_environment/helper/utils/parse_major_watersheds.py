import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_major_watersheds(iso3Code: str) -> dict:
    """Parse major watersheds from CIA Environment section for a given country."""
    result = {
        "major_watersheds": {
            "watersheds": [],
            "raw_text": None
        },
        "major_watersheds_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    watershed_data = environment_section.get('Major watersheds (area sq km)', {})

    if not watershed_data or not isinstance(watershed_data, dict):
        return result

    text = watershed_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['major_watersheds']['raw_text'] = cleaned

        # Parse pattern: "Name (area sq km)" or "Name* (area sq km)"
        pattern = re.compile(r'([A-Za-z\s\*\']+?)\s*\(([\d,]+)\s*sq\s*km', re.IGNORECASE)
        matches = pattern.findall(cleaned)

        for name, area in matches:
            name = name.strip().rstrip('*')
            if name:
                result['major_watersheds']['watersheds'].append({
                    'name': name,
                    'area_sq_km': int(area.replace(',', ''))
                })

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_major_watersheds")
    print("="*60)
    for iso3 in ['USA', 'BRA', 'RUS', 'CHN', 'IND', 'DEU']:
        print(f"\n{iso3}:")
        try:
            result = parse_major_watersheds(iso3)
            if result and result['major_watersheds']['watersheds']:
                mw = result['major_watersheds']
                print(f"  Found {len(mw['watersheds'])} watersheds:")
                for ws in mw['watersheds'][:3]:
                    print(f"    - {ws['name']}: {ws['area_sq_km']:,} sq km")
            else:
                print("  No watersheds data")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
