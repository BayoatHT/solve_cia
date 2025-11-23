import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_credit_ratings(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses credit ratings data into a structured nested dictionary format.

    Parameters:
        pass_data (dict): The dictionary containing credit ratings data.

    Returns:
        dict: A nested dictionary with parsed credit ratings information.
    """
    result = {
        "credit_ratings_note": "",
        "credit_fitch_rating": {},
        "credit_moodys_rating": {},
        "credit_standard_poor_rating": {}
    }

    # Parse the note if present
    result["credit_ratings_note"] = clean_text(pass_data.get("note", ""))

    # Helper function to parse rating and year from text
    def parse_rating(text: str) -> dict:
        match = re.match(r"([A-Za-z+]+)\s*\((\d{4})\)", text)
        if match:
            return {
                "rating": match.group(1),
                "year": int(match.group(2))
            }
        return {"rating": "", "year": 0}

    # Parse each rating if present
    if "Fitch rating" in pass_data:
        result["credit_fitch_rating"] = parse_rating(
            pass_data["Fitch rating"].get("text", ""))
    if "Moody's rating" in pass_data:
        result["credit_moodys_rating"] = parse_rating(
            pass_data["Moody's rating"].get("text", ""))
    if "Standard & Poors rating" in pass_data:
        result["credit_standard_poor_rating"] = parse_rating(
            pass_data["Standard & Poors rating"].get("text", ""))

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 6 >>> 'Credit ratings'
    # --------------------------------------------------------------------------------------------------
    # "Fitch rating" - 'credit_fitch_rating'
    # "Moody's rating" - 'credit_moodys_rating'
    # "Standard & Poors rating" - 'credit_standard_poor_rating'
    # "note" - 'credit_ratings_note'
    # --------------------------------------------------------------------------------------------------
    # ['credit_fitch_rating', 'credit_moodys_rating', 'credit_standard_poor_rating', 'credit_ratings_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Fitch rating": {
            "text": "AAA (1994)"
        },
        "Moody's rating": {
            "text": "Aaa (1949)"
        },
        "Standard & Poors rating": {
            "text": "AA+ (2011)"
        },
        "note": "<strong>note: </strong>The year refers to the year in which the current credit rating was first obtained."
    }
    parsed_data = parse_credit_ratings(pass_data)
    print(parsed_data)
