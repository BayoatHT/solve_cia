import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_industrial_production(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses the industrial production growth rate data into a structured format.

    Parameters:
        pass_data (dict): The dictionary containing industrial production data.

    Returns:
        dict: A dictionary containing the growth rate, year, and any associated note.
    """
    result = {}

    # Process the "text" field
    text = pass_data.get("text", "")
    if text:
        match = re.match(r"([-\d.]+)% \((\d{4}) est\.\)", text)
        if match:
            result["industrial_production_growth_rate"] = {
                "value": float(match.group(1)),
                "year": int(match.group(2)),
                "unit": "%"
            }

    # Process the "note" field
    note = pass_data.get("note", "")
    if note:
        result["industrial_production_growth_rate_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 27 >>> 'Industrial production growth rate'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'industrial_production_growth_rate_note'
    # "text" - 'industrial_production_growth_rate'
    # --------------------------------------------------------------------------------------------------
    # ['industrial_production_growth_rate', 'industrial_production_growth_rate_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "3.25% (2021 est.)",
        "note": "<b>note:</b> annual % change in industrial value added based on constant local currency"
    }
    parsed_data = parse_industrial_production(pass_data)
    print(parsed_data)
