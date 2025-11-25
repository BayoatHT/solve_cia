import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_transportation_note(iso3Code: str, return_original: bool = False)-> dict:
    """Parse Transportation - note from CIA Transportation section for a given country."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    transport_section = raw_data.get('Transportation', {})
    note_data = transport_section.get('Transportation - note', {})

    if return_original:
        return note_data


    if not note_data:
        return result

    try:
        if isinstance(note_data, dict) and 'text' in note_data:
            text = note_data['text']
            if text and isinstance(text, str):
                result['transportation_note'] = clean_text(text)
        elif isinstance(note_data, str):
            result['transportation_note'] = clean_text(note_data)

    except Exception as e:
        logger.error(f"Error parsing transportation_note for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_transportation_note")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'RUS', 'BRA', 'IND', 'WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_transportation_note(iso3)
            if result:
                for key, val in result.items():
                    val_str = str(val)
                    print(f"  {key}: {val_str[:80] if len(val_str) > 80 else val_str}...")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
