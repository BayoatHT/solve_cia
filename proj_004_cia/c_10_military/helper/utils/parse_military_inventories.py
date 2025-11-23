import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_inventories(military_inventories_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Military Inventories' data into a structured dictionary.

    Parameters:
        military_inventories_data (dict): The 'Military Inventories' section from the data.

    Returns:
        dict: A dictionary containing structured information on the military inventory.
    """
    result = {
        "military_equip": [],
        "military_note": ""
    }

    # Extract and parse the main text information
    text = military_inventories_data.get("text", "")
    if text:
        # Extract the year if present at the end
        result["military_equip"] = parse_text_to_list(
            text)

    # Handle notes
    note_text = military_inventories_data.get("note", "")
    if note_text:
        clean_overview_note = re.sub(
            r'<strong>note:</strong>\s*', '', note_text, flags=re.IGNORECASE)
        result["military_note"] = clean_text(
            clean_overview_note)

    return result


# Example usage
if __name__ == "__main__":
    # ['mil_equip', 'mil_equip_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    military_inventories_data = {
        "text": "the US military's inventory is comprised almost entirely of domestically produced weapons systems (some assembled with foreign components) along with a smaller mix of imported equipment from a variety of Western countries such as Germany and the UK; the US defense industry is capable of designing, developing, maintaining, and producing the full spectrum of weapons systems; the US is the world's leading arms exporter (2024)",
        "note": ""
    }
    parsed_data = parse_military_inventories(military_inventories_data)
    print(parsed_data)
