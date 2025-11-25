import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_terrorism(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse terrorism data from CIA Terrorism section for a given country.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'AFG')

    Returns:
        dict: A dictionary containing parsed information for terrorist groups and notes.
    """
    result = {
        "terror_groups": [],
        "terror_groups_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    terrorism_section = raw_data.get('Terrorism', {})
    terror_data = terrorism_section.get('Terrorist group(s)', {})

    if return_original:
        return terror_data


    if not terror_data or not isinstance(terror_data, dict):
        return result

    try:
        # Handle 'text'
        terror_text = terror_data.get("text", "")
        if terror_text:
            result["terror_groups"] = parse_text_to_list(terror_text)

        # Handle 'note'
        terror_note = terror_data.get("note", "")
        if terror_note:
            # Remove '<strong>note:</strong>' if present
            clean_note = re.sub(r'<strong>note:</strong>\s*',
                                '', terror_note, flags=re.IGNORECASE)
            result["terror_groups_note"] = clean_text(clean_note)

    except Exception as e:
        logger.error(f"Error parsing terrorism for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_terrorism")
    print("=" * 60)
    for iso3 in ['USA', 'AFG', 'IRQ', 'SYR', 'PAK', 'NGA']:
        print(f"\n{iso3}:")
        try:
            result = parse_terrorism(iso3)
            if result.get('terror_groups'):
                groups = result['terror_groups']
                print(f"  Groups: {len(groups)}")
                for g in groups[:3]:
                    print(f"    - {str(g)[:50]}...")
            else:
                print("  No terrorism data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
