import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def split_notes(note_text: str) -> list:
    """
    Splits a note text into individual notes based on <br><br> tags,
    and removes <strong> tags and any content inside them.

    Parameters:
        note_text (str): The raw note text to be split.

    Returns:
        list: A list of cleaned notes.
    """
    # Split the text into parts at <br><br> tags
    parts = note_text.split('<br><br>')
    # Clean each part by removing <strong> tags and their content
    cleaned_notes = [clean_text(re.sub(r'<strong>.*?</strong>', '', part, flags=re.IGNORECASE))
                     for part in parts if part.strip()]
    return cleaned_notes


def parse_military_age(iso3Code: str) -> dict:
    """
    Parse military age and service obligation data from CIA Military and Security section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary containing parsed information for military age requirements and notes.
    """
    result = {
        "mil_age": [],
        "mil_age_notes": []
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    military_age_data = military_section.get('Military service age and obligation', {})

    if not military_age_data or not isinstance(military_age_data, dict):
        return result

    try:
        # Handle 'text'
        age_text = military_age_data.get("text", "")
        if age_text:
            result["mil_age"] = parse_text_to_list(age_text)

        # Handle 'note'
        age_note = military_age_data.get("note", "")
        if age_note:
            result["mil_age_notes"] = split_notes(age_note)

    except Exception as e:
        logger.error(f"Error parsing military age for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_age")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'DEU', 'GBR', 'ISR']:
        print(f"\n{iso3}:")
        try:
            result = parse_military_age(iso3)
            if result.get('mil_age'):
                age_info = result['mil_age']
                print(f"  Age entries: {len(age_info)}")
                if age_info:
                    print(f"    First: {str(age_info[0])[:60]}...")
            else:
                print("  No age data found")
            if result.get('mil_age_notes'):
                print(f"  Notes: {len(result['mil_age_notes'])}")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
