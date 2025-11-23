import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_exports_partners(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the exports partners data including export partners, their share percentages, and any additional notes.

    Parameters:
        pass_data (dict): The dictionary containing export partners data.

    Returns:
        dict: A dictionary with parsed export partners data.
    """
    result = {}

    # Handle the 'note' key if it exists
    if "note" in pass_data:
        result["exports_partners_note"] = clean_text(pass_data.get("note", ""))

    # Parse the main text for partners and year
    text = pass_data.get("text", "")
    if text:
        # Check for year in parentheses at the end of the text
        match = re.search(r"\((\d{4})\)$", text)
        if match:
            # Extract and set the year
            result["exports_partners"] = {
                "date": int(match.group(1))
            }
            # Remove the year from the main text
            partners_text = text[:match.start()].strip()
        else:
            partners_text = text

        # Split the remaining text by commas to get partner and percentage pairs
        partners_list = []
        for entry in partners_text.split(","):
            entry = entry.strip()
            # Match the pattern for 'Country %'
            partner_match = re.match(r"(.+?)\s(\d+)%", entry)
            if partner_match:
                country = partner_match.group(1).strip()
                percentage = int(partner_match.group(2))
                partners_list.append(
                    {"country": country, "percentage": percentage})

        # Store the list of partners in the result
        result["exports_partners"]["partners"] = partners_list

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 14 >>> 'Exports - partners'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'exports_partners_note'
    # "text" - 'exports_partners'
    # --------------------------------------------------------------------------------------------------
    # ['exports_partners', 'exports_partners_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "Canada 16%, Mexico 15%, China 8%, Japan 4%, UK 4% (2022)",
        "note": "<b>note:</b> top five export partners based on percentage share of exports"
    }
    parsed_data = parse_exports_partners(pass_data)
    print(parsed_data)
