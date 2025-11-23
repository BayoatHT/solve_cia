import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_current_account_balance(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Current account balance' data into a structured dictionary format.

    Parameters:
        pass_data (dict): The dictionary containing current account balance data.

    Returns:
        dict: A dictionary with parsed account balance information, including values by year and a note.
    """
    result = {}

    # Handle the 'note' key if it exists
    if "note" in pass_data:
        result["current_account_balance_note"] = clean_text(
            pass_data.get("note", ""))

    # Helper function to parse balance entry
    def parse_balance_entry(text: str) -> dict:
        # Match amounts in billions with optional parentheses around year
        match = re.match(
            r"([-]?\$?[\d,]+\.\d+)\s*billion\s*\(?(\d{4})\)?", text)
        if match:
            # Extract and clean value
            value_str = match.group(1).replace("$", "").replace(",", "")
            value = float(value_str) if value_str else 0
            year = int(match.group(2)) if match.group(2) else 0
            return {
                "value": value,
                "unit": "billion USD",
                "year": year
            }
        return {"value": 0, "unit": "billion USD", "year": 0}

    # Parse each "Current account balance YEAR" entry
    for key, value in pass_data.items():
        if key.startswith("Current account balance") and "text" in value:
            year = key.split()[-1]  # Extract year from the key
            result[f"current_account_balance_{year}"] = parse_balance_entry(
                value["text"])

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Current account balance 2023" - 'current_account_balance_2023'
    # "note" -  'current_account_balance_note'
    # --------------------------------------------------------------------------------------------------
    # ['current_account_balance_2023', 'current_account_balance_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Current account balance 2023": {
            "text": "-$818.822 billion (2023 est.)"
        },
        "Current account balance 2022": {
            "text": "-$971.594 billion (2022 est.)"
        },
        "Current account balance 2021": {
            "text": "-$831.453 billion (2021 est.)"
        },
        "note": "<b>note:</b> balance of payments - net trade and primary/secondary income in current dollars"
    }
    parsed_data = parse_current_account_balance(pass_data)
    print(parsed_data)
