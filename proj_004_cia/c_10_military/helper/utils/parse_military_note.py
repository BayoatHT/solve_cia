import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_military_note(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse military note data from CIA Military and Security section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary where each note is organized by 'note_1', 'note_2', etc.
    """
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    military_note_data = military_section.get('Military - note', {})

    if return_original:
        return military_note_data


    if not military_note_data or not isinstance(military_note_data, dict):
        return result

    try:
        text = military_note_data.get("text", "")
        if not text:
            return result

        # Split by <br><br> to separate paragraphs and potential notes
        paragraphs = re.split(r'<br\s*/?><br\s*/?>', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        note_counter = 1  # Counter to handle notes without specified numbers
        for paragraph in paragraphs:
            # Check if the paragraph has a strong tag with a note number
            match = re.match(r'<strong>(note \d+):</strong>\s*(.*)',
                             paragraph, re.IGNORECASE)
            if match:
                # Extract the note key and content
                note_key = match.group(1).replace(
                    " ", "_").lower()  # e.g., "note_1"
                note_content = match.group(2)
            else:
                # Handle paragraphs without a note number
                note_key = f"military_note_{note_counter}"
                note_content = paragraph
                note_counter += 1

            # Clean HTML tags and split content by semicolons into items
            cleaned_content = clean_text(note_content)
            note_items = [item.strip()
                          for item in cleaned_content.split(';') if item.strip()]

            # Store items in result dictionary
            result[note_key] = note_items

    except Exception as e:
        logger.error(f"Error parsing military note for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_note")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'DEU', 'GBR', 'FRA']:
        print(f"\n{iso3}:")
        try:
            result = parse_military_note(iso3)
            if result:
                print(f"  Notes: {len(result)} sections")
                for key in list(result.keys())[:2]:
                    items = result[key]
                    if items:
                        print(f"    {key}: {items[0][:50]}...")
            else:
                print("  No notes found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
