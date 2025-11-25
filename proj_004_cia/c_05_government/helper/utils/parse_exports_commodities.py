import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_exports_commodities(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """
    Parses the exports commodities data including the main export commodities and any additional notes.

    Parameters:
        test_data (dict): The dictionary containing export commodities data.

    Returns:
        dict: A dictionary with parsed export commodities data.
    """
    if return_original:
        return test_data

    result = {}

    # Handle the 'note' key if it exists
    if "note" in test_data:
        result["exports_commodities_note"] = clean_text(
            test_data.get("note", ""))

    # Parse the main text for commodities and date
    text = test_data.get("text", "")
    if text:
        # Check for year in parentheses at the end of the text
        match = re.search(r"\((\d{4})\)$", text)
        if match:
            # Extract and set the year
            result["exports_commodities"] = {
                "date": int(match.group(1))
            }
            # Remove the year from the main text
            commodities_text = text[:match.start()].strip()
        else:
            commodities_text = text

        # Split the remaining text by commas to get commodities list
        commodities_list = [commodity.strip() for commodity in commodities_text.split(
            ",") if commodity.strip()]
        result["exports_commodities"]["commodities"] = commodities_list

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 13 >>> 'Exports - commodities'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'exports_commodities_note'
    # "text" - 'exports_commodities'
    # --------------------------------------------------------------------------------------------------
    # ['exports_commodities', 'exports_commodities_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "refined petroleum, crude petroleum, natural gas, cars, integrated circuits (2022)",
        "note": "<b>note:</b> top five export commodities based on value in dollars"
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
