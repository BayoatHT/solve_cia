import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_imports(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses the imports data into a structured format.

    Parameters:
        pass_data (dict): The dictionary containing imports data.

    Returns:
        dict: A dictionary containing the imports data by year and any associated note.
    """
    result = {}

    # Process each key-value pair in pass_data
    for key, value in pass_data.items():
        if key.startswith("Imports"):
            # Extract the year from the key
            year_match = re.search(r"(\d{4})", key)
            year = year_match.group(1) if year_match else "unknown"

            # Extract the value from the text field
            text = value.get("text", "")
            amount_match = re.match(r"\$([\d,\.]+) trillion", text)
            if amount_match:
                amount = float(amount_match.group(1).replace(",", ""))
                result[f"imports_{year}"] = {
                    "value": amount,
                    "unit": "trillion USD",
                    "year": int(year)
                }

    # Process the "note" field
    note = pass_data.get("note", "")
    if note:
        result["imports_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 24 >>> 'Imports'
    # --------------------------------------------------------------------------------------------------
    # "Imports 2023" - 'imports_2023'
    # "note" - 'imports_note'
    # --------------------------------------------------------------------------------------------------
    # ['imports_2023', 'imports_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Imports 2023": {
            "text": "$3.832 trillion (2023 est.)"
        },
        "Imports 2022": {
            "text": "$3.97 trillion (2022 est.)"
        },
        "Imports 2021": {
            "text": "$3.409 trillion (2021 est.)"
        },
        "note": "<b>note:</b> balance of payments - imports of goods and services in current dollars"
    }
    parsed_data = parse_imports(pass_data)
    print(parsed_data)
