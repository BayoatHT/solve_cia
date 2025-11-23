import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_international(international_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to international disputes, including the main text and any associated note.

    Parameters:
        international_data (dict): The dictionary containing international disputes data.

    Returns:
        dict: A dictionary containing parsed information for international disputes and notes.
    """
    result = {
        "international": [],
        "international_note": ""
    }

    # Handle main 'text'
    international_text = international_data.get("text", "")
    if international_text:
        result["international"] = parse_text_to_list(international_text)

    # Handle 'note'
    international_note = international_data.get("note", "")
    if international_note:
        result["international_note"] = clean_text(international_note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 1 >>> 'Disputes - international'
    # >>> ['disputes_international', 'disputes_international_note']
    # --------------------------------------------------------------------------------------------------
    international_data = {
        "text": "++ many neighboring states reject Moroccan administration of Western Sahara; several states have extended diplomatic relations to the \"Sahrawi Arab Democratic Republic\" represented by the Polisario Front in exile in Algeria, while others support Morocco's proposal to grant the territory autonomy as part of Morocco, although no state recognizes Moroccan sovereignty over Western Sahara; an estimated 100,000 Sahrawi refugees continue to be sheltered in camps in Tindouf, Algeria, which has hosted Sahrawi refugees since the 1980s",
        "note": ""
    }
    parsed_data = parse_international(international_data)
    print(parsed_data)
