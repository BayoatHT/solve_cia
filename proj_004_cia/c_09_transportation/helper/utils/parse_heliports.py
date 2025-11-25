import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_heliports(iso3Code: str, return_original: bool = False)-> dict:
    """Parse Heliports from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    pass_data = transport_section.get('Heliports', {})

    if return_original:
        return pass_data


    if not pass_data:
        return result

    try:
        # Parse the main text field
        if isinstance(pass_data, dict) and 'text' in pass_data:
            text = pass_data['text']
            parsed = parse_transport_value(text)

            if parsed['value'] is not None:
                result['heliports_total_value'] = int(parsed['value'])
            if parsed['year']:
                result['heliports_total_year'] = parsed['year']
            if parsed['is_estimate']:
                result['heliports_total_is_estimate'] = parsed['is_estimate']

        # Parse note if present
        if isinstance(pass_data, dict) and 'note' in pass_data:
            note = pass_data['note']
            if note and isinstance(note, str) and note.strip():
                result['heliports_total_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing parse_heliports for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_heliports")
    print("="*60)
    for iso3 in ['USA', 'BRA', 'CHN', 'RUS', 'IND', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_heliports(iso3)
            if result:
                for key, val in result.items():
                    if isinstance(val, (int, float)):
                        print(f"  {key}: {val:,.0f}")
                    else:
                        print(f"  {key}: {val[:80] if isinstance(val, str) and len(val) > 80 else val}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
