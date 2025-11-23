import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_exports_commodities(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the exports commodities data including the main export commodities and any additional notes.

    Parameters:
        pass_data (dict): The dictionary containing export commodities data.

    Returns:
        dict: A dictionary with parsed export commodities data.
    """
    result = {}

    # Handle the 'note' key if it exists
    if "note" in pass_data:
        result["exports_commodities_note"] = clean_text(
            pass_data.get("note", ""))

    # Parse the main text for commodities and date
    text = pass_data.get("text", "")
    if text:
        # Check for year in parentheses at the end of the text
        # Handle formats like "(2022)", "(2012 est.)", or no year at all
        match = re.search(r"\((\d{4})(?:\s*est\.?)?\)\s*$", text)
        if match:
            year = int(match.group(1))
            # Remove the year from the main text
            commodities_text = text[:match.start()].strip()
        else:
            year = None
            commodities_text = text

        # Split the remaining text by commas to get commodities list
        commodities_list = [commodity.strip() for commodity in commodities_text.split(
            ",") if commodity.strip()]

        # Build the result dict (always create the dict first)
        result["exports_commodities"] = {
            "commodities": commodities_list
        }
        if year:
            result["exports_commodities"]["date"] = year

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 13 >>> 'Exports - commodities'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'exports_commodities_note'
    # "text" - 'exports_commodities'
    # --------------------------------------------------------------------------------------------------
    # ['exports_commodities', 'exports_commodities_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "refined petroleum, crude petroleum, natural gas, cars, integrated circuits (2022)",
        "note": "<b>note:</b> top five export commodities based on value in dollars"
    }
    parsed_data = parse_exports_commodities(pass_data)
    print(parsed_data)
