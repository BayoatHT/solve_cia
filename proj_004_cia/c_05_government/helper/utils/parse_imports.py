import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_imports(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """
    Parses the imports data into a structured format.

    Parameters:
        test_data (dict): The dictionary containing imports data.

    Returns:
        dict: A dictionary containing the imports data by year and any associated note.
    """
    if return_original:
        return test_data

    result = {}

    # Process each key-value pair in test_data
    for key, value in test_data.items():
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
    note = test_data.get("note", "")
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
    test_data = {
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
