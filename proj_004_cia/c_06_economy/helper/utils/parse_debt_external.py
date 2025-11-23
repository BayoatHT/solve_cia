import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_debt_external(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses 'Debt - external' data including year-specific debt amounts and any additional notes.

    Parameters:
        pass_data (dict): The dictionary containing external debt data.

    Returns:
        dict: A dictionary with parsed debt data by year and notes if available.
    """
    result = {}

    # Handle the 'note' key if it exists
    if "note" in pass_data:
        result["debt_external_note"] = clean_text(pass_data.get("note", ""))

    # Helper function to parse debt entry
    def parse_debt_entry(text: str) -> dict:
        # Match amounts in trillions or billions with optional parentheses around year
        match = re.match(r"\$([\d,]+)\s*\(?(\d{4})?\)?", text)
        if match:
            # Extract and clean the value
            value_str = match.group(1).replace(",", "")
            # Convert to trillions
            value = float(value_str) / 1_000_000_000_000
            year = int(match.group(2)) if match.group(2) else 0
            return {
                "value": value,
                "unit": "trillion USD",
                "year": year
            }
        return {"value": 0, "unit": "trillion USD", "year": 0}

    # Parse each "Debt - external YEAR" entry
    for key, value in pass_data.items():
        if key.startswith("Debt - external") and "text" in value:
            year = key.split()[-1]  # Extract year from the key
            result[f"debt_external_{year}"] = parse_debt_entry(value["text"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 8 >>> 'Debt - external'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Debt - external 2019": {
            "text": "$20,275,951,000,000 (2019 est.)"
        },
        "Debt - external 2018": {
            "text": "$19,452,478,000,000 (2018 est.)"
        },
        "note": "<strong>note:</strong> approximately 4/5ths of US external debt is denominated in US dollars; foreign lenders have been willing to hold US dollar denominated debt instruments because they view the dollar as the world's reserve currency"
    }
    parsed_data = parse_debt_external(pass_data)
    print(parsed_data)
