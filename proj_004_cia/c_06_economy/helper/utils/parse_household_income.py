import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_household_income(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses household income data by extracting the income share for the highest and lowest 10% 
    and any associated notes.

    Parameters:
        pass_data (dict): The dictionary containing household income data.

    Returns:
        dict: A dictionary with extracted income share information and note.
    """
    result = {}

    # Loop through each key-value pair in pass_data
    for key, value in pass_data.items():
        if key == "lowest 10%":
            # Extract percentage and year from "lowest 10%" text field
            text = value.get("text", "")
            match = re.match(r"([\d\.]+)% \((\d{4}) est.\)", text)
            if match:
                result["house_income_lowest_10"] = {
                    "value": float(match.group(1)),
                    "unit": "%",
                    "year": int(match.group(2))
                }

        elif key == "highest 10%":
            # Extract percentage and year from "highest 10%" text field
            text = value.get("text", "")
            match = re.match(r"([\d\.]+)% \((\d{4}) est.\)", text)
            if match:
                result["house_income_highest_10"] = {
                    "value": float(match.group(1)),
                    "unit": "%",
                    "year": int(match.group(2))
                }

        elif key == "note":
            # Clean and store the note
            result["house_income_note"] = clean_text(value)

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "highest 10%" - 'house_income_highest_10'
    # "lowest 10%" - 'house_income_lowest_10'
    # "note" - 'house_income_note'
    # --------------------------------------------------------------------------------------------------
    # ['house_income_highest_10', 'house_income_lowest_10', 'house_income_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "lowest 10%": {
            "text": "2.2% (2021 est.)"
        },
        "highest 10%": {
            "text": "30.1% (2021 est.)"
        },
        "note": "<b>note:</b> % share of income accruing to lowest and highest 10% of population"
    }
    parsed_data = parse_household_income(pass_data)
    print(parsed_data)
