import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_terrorism(terror_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to terrorism, including terrorist groups and associated notes.

    Parameters:
        terror_data (dict): The dictionary containing terrorism data.

    Returns:
        dict: A dictionary containing parsed information for terrorist groups and notes.
    """
    result = {
        "terror_groups": [],
        "terror_groups_note": ""
    }

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

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # ['terror_groups', 'terror_groups_note']
    # --------------------------------------------------------------------------------------------------
    terror_data = {
        "text": "Islamic Revolutionary Guard Corps/Qods Force; Islamic State of Iraq and ash-Sham (ISIS); al-Qa'ida",
        "note": "<strong>note:</strong> details about the history, aims, leadership, organization, areas of operation, tactics, targets, weapons, size, and sources of support of the group(s) appear(s) in the Terrorism reference guide"
    }
    parsed_data = parse_terrorism(terror_data)
    print(parsed_data)
