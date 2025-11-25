import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_geoparks(iso3Code: str, return_original: bool = False)-> dict:
    """Parse geoparks from CIA Environment section for a given country."""
    result = {
        "geoparks": {
            "total": None,
            "parks": [],
            "raw_text": None
        },
        "geoparks_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    geoparks_data = environment_section.get('Geoparks', {})

    if return_original:
        return geoparks_data


    if not geoparks_data or not isinstance(geoparks_data, dict):
        return result

    # Parse total
    total_data = geoparks_data.get('total global geoparks and regional networks', {})
    if total_data and isinstance(total_data, dict):
        text = total_data.get('text', '')
        if text and text.upper() != 'NA':
            num_match = re.search(r'(\d+)', text)
            if num_match:
                result['geoparks']['total'] = int(num_match.group(1))

    # Parse individual geoparks
    parks_data = geoparks_data.get('global geoparks and regional networks', {})
    if parks_data and isinstance(parks_data, dict):
        text = parks_data.get('text', '')
        if text and text.upper() != 'NA':
            cleaned = clean_text(text)
            result['geoparks']['raw_text'] = cleaned
            # Split by semicolon
            parks = [p.strip() for p in cleaned.split(';') if p.strip()]
            result['geoparks']['parks'] = parks

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_geoparks")
    print("="*60)
    # Geoparks are rare - test countries that might have them
    for iso3 in ['CHN', 'DEU', 'FRA', 'ESP', 'ITA', 'USA']:
        print(f"\n{iso3}:")
        try:
            result = parse_geoparks(iso3)
            if result and result['geoparks']['total']:
                gp = result['geoparks']
                print(f"  Total: {gp['total']} geoparks")
                for park in gp['parks'][:3]:
                    print(f"    - {park[:50]}...")
            else:
                print("  No geoparks data")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
