import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_note(military_note_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'military note' data into a structured dictionary of notes.

    Parameters:
        military_note_data (dict): The dictionary containing the 'text' field for military notes.

    Returns:
        dict: A dictionary where each note is organized by 'note_1', 'note_2', etc., each containing a list of items.
    """
    result = {}

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

    return result


# Example usage
if __name__ == "__main__":
    military_note_data = {
        "text": "the US is a member of NATO and was one of the original 12 countries to sign the North Atlantic Treaty (also known as the Washington Treaty) in 1949<br><br>the US military's primary missions are to deter potential enemies, provide for the defense of the US, the Territories, Commonwealths and possessions, and any areas occupied by the US, and to protect US national interests; it has worldwide responsibilities; the separate services operate jointly under 11 regional- or functionally-based joint service \"combatant\" commands: Africa Command; Central Command, Cyber Command, European Command, Indo-Pacific Command, Northern Command, Southern Command, Space Command, Special Operations Command, Strategic Command, and Transportation Command<br><br>Congress officially created the US military in September 1789; the US Army was established in June 1775 as the Continental Army; after the declaration of independence in July 1776, the Continental Army and the militia in the service of Congress became known collectively as the Army of the United States; when Congress ordered the Continental Army to disband in 1784, it retained a small number of personnel that would form the nucleus of the 1st American Regiment for national service formed later that year; both the US Navy and the US Marines were also established in 1775, but the Navy fell into disuse after the Revolutionary War, and was reestablished by Congress in 1794; the first US military unit devoted exclusively to aviation began operations in 1913 as part of the US Army; the Army Air Corps (AAC) was the US military service dedicated to aerial warfare between 1926 and 1941; the AAC became the US Army Air Forces in 1941 and remained as a combat arm of the Army until the establishment of the US Air Force in 1947 (2024)"
    }
    parsed_data = parse_military_note(military_note_data)
    print(parsed_data)
