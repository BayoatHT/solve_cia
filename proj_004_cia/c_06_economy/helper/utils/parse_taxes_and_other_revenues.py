import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_taxes_and_other_revenues(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses the taxes and other revenues data, extracting the percentage, year, and any associated notes.

    Parameters:
        pass_data (dict): The dictionary containing taxes and other revenues data.

    Returns:
        dict: A dictionary with parsed data for taxes and other revenues.
    """
    result = {}

    # Process 'text' field for percentage and year
    text = pass_data.get("text", "")
    match = re.match(r"([\d.]+)%\s*\(of GDP\)\s*\((\d{4})", text)
    if match:
        result["taxes_revenues"] = {
            "value": float(match.group(1)),
            "unit": "% of GDP",
            "year": int(match.group(2))
        }
    else:
        logging.warning(f"Unexpected format in 'text' data: {text}")

    # Process 'note' field
    note = pass_data.get("note", "")
    if note:
        result["taxes_revenues_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 39 >>> 'Taxes and other revenues'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'taxes_revenues_note'
    # "text" - 'taxes_revenues'
    # --------------------------------------------------------------------------------------------------
    # ['taxes_revenues', 'taxes_revenues_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "19.65% (of GDP) (2022 est.)",
        "note": "<b>note:</b> central government tax revenue as a % of GDP"
    }
    parsed_data = parse_taxes_and_other_revenues(pass_data)
    print(parsed_data)
