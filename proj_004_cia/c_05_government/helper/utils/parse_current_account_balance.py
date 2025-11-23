import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_current_account_balance(test_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Current account balance' data into a structured dictionary format.

    Parameters:
        test_data (dict): The dictionary containing current account balance data.

    Returns:
        dict: A dictionary with parsed account balance information, including values by year and a note.
    """
    result = {}

    # Handle the 'note' key if it exists
    if "note" in test_data:
        result["current_account_balance_note"] = clean_text(
            test_data.get("note", ""))

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
    for key, value in test_data.items():
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
    test_data = {
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
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Capital'
    # --------------------------------------------------------------------------------------------------
    # List of countries to test
    test_countries = ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'IND'
                      'RUS', 'BRA', 'JPN', 'AUS', 'CAN', 'MEX'
                      'ZAF', 'KOR', 'ITA', 'ESP', 'NLD', 'SWE',
                      'NOR', 'FIN', 'DNK', 'POL', 'TUR', 'ARG',
                      'CHL', 'PER', 'COL', 'VEN', 'EGY', 'SAR',
                      'UAE', 'ISR', 'IRN', 'PAK', 'BGD', 'PHL',
                      'IDN', 'MYS', 'THA', 'VNM', 'SGP', 'NZL',
                      'KHM', 'MMR', 'LKA', 'NPL', 'BTN', 'MDV',
                      'KAZ', 'UZB', 'TKM', 'KGZ', 'TJK', 'AZE',
                      'GEO', 'ARM', 'MDA', 'UKR', 'BLR', 'LVA',]
    # --------------------------------------------------------------------------------------------------
    test_capital_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Admin Divisions Orginal Data")
    for index, country_data in enumerate(test_capital_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    print("Testing Capital Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_capital_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_capital(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
