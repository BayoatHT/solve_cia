import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_military_inventories(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse military equipment inventories data from CIA Military and Security section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary containing structured information on the military inventory.
    """
    result = {
        "military_equip": [],
        "military_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    military_inventories_data = military_section.get('Military equipment inventories and acquisitions', {})

    if return_original:
        return military_inventories_data


    if not military_inventories_data or not isinstance(military_inventories_data, dict):
        return result

    try:
        # Extract and parse the main text information
        text = military_inventories_data.get("text", "")
        if text:
            result["military_equip"] = parse_text_to_list(text)

        # Handle notes
        note_text = military_inventories_data.get("note", "")
        if note_text:
            clean_overview_note = re.sub(
                r'<strong>note:</strong>\s*', '', note_text, flags=re.IGNORECASE)
            result["military_note"] = clean_text(clean_overview_note)

    except Exception as e:
        logger.error(f"Error parsing military inventories for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_inventories")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'DEU', 'GBR', 'IND']:
        print(f"\n{iso3}:")
        try:
            result = parse_military_inventories(iso3)
            if result.get('military_equip'):
                equip = result['military_equip']
                print(f"  Equipment entries: {len(equip)}")
                if equip:
                    print(f"    First: {str(equip[0])[:60]}...")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
