import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_industries(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses the industries data into an array of strings split by semicolons.

    Parameters:
        pass_data (dict): The dictionary containing industries data.

    Returns:
        dict: A dictionary containing a list of industries and any note.
    """
    result = {}

    # Process text field with parse_text_to_list if available
    text = pass_data.get("text", "")
    if text:
        result["industries"] = parse_text_to_list(text)

    # Process note field with clean_text if available
    note = pass_data.get("note", "")
    if note:
        result["industries_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 28 >>> 'Industries'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'industries_note'
    # "text" - 'industries'
    # --------------------------------------------------------------------------------------------------
    # ['industries', 'industries_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "highly diversified, world leading, high-technology innovator, second-largest industrial output in the world; petroleum, steel, motor vehicles, aerospace, telecommunications, chemicals, electronics, food processing, consumer goods, lumber, mining"
    }
    parsed_data = parse_industries(pass_data)
    print(parsed_data)
