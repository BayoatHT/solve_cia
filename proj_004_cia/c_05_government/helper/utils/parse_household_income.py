import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_household_income(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parses household income data by extracting the income share for the highest and lowest 10% 
    and any associated notes.

    Parameters:
        test_data (dict): The dictionary containing household income data.

    Returns:
        dict: A dictionary with extracted income share information and note.
    """
    result = {}

    # Loop through each key-value pair in test_data
    for key, value in test_data.items():
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
    test_data = {
        "lowest 10%": {
            "text": "2.2% (2021 est.)"
        },
        "highest 10%": {
            "text": "30.1% (2021 est.)"
        },
        "note": "<b>note:</b> % share of income accruing to lowest and highest 10% of population"
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
