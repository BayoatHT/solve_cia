import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_debt_external(test_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses 'Debt - external' data including year-specific debt amounts and any additional notes.

    Parameters:
        test_data (dict): The dictionary containing external debt data.

    Returns:
        dict: A dictionary with parsed debt data by year and notes if available.
    """
    if return_original:
        return test_data

    result = {}

    # Handle the 'note' key if it exists
    if "note" in test_data:
        result["debt_external_note"] = clean_text(test_data.get("note", ""))

    # Helper function to parse debt entry
    def parse_debt_entry(text: str, return_original: bool = False)-> dict:
        # Match amounts in trillions or billions with optional parentheses around year
        if return_original:
            return text

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
    for key, value in test_data.items():
        if key.startswith("Debt - external") and "text" in value:
            year = key.split()[-1]  # Extract year from the key
            result[f"debt_external_{year}"] = parse_debt_entry(value["text"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 8 >>> 'Debt - external'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    test_data = {
        "Debt - external 2019": {
            "text": "$20,275,951,000,000 (2019 est.)"
        },
        "Debt - external 2018": {
            "text": "$19,452,478,000,000 (2018 est.)"
        },
        "note": "<strong>note:</strong> approximately 4/5ths of US external debt is denominated in US dollars; foreign lenders have been willing to hold US dollar denominated debt instruments because they view the dollar as the world's reserve currency"
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
