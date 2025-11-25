import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_exports_partners(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """
    Parses the exports partners data including export partners, their share percentages, and any additional notes.

    Parameters:
        test_data (dict): The dictionary containing export partners data.

    Returns:
        dict: A dictionary with parsed export partners data.
    """
    if return_original:
        return test_data

    result = {}

    # Handle the 'note' key if it exists
    if "note" in test_data:
        result["exports_partners_note"] = clean_text(test_data.get("note", ""))

    # Parse the main text for partners and year
    text = test_data.get("text", "")
    if text:
        # Check for year in parentheses at the end of the text
        match = re.search(r"\((\d{4})\)$", text)
        if match:
            # Extract and set the year
            result["exports_partners"] = {
                "date": int(match.group(1))
            }
            # Remove the year from the main text
            partners_text = text[:match.start()].strip()
        else:
            partners_text = text

        # Split the remaining text by commas to get partner and percentage pairs
        partners_list = []
        for entry in partners_text.split(","):
            entry = entry.strip()
            # Match the pattern for 'Country %'
            partner_match = re.match(r"(.+?)\s(\d+)%", entry)
            if partner_match:
                country = partner_match.group(1).strip()
                percentage = int(partner_match.group(2))
                partners_list.append(
                    {"country": country, "percentage": percentage})

        # Store the list of partners in the result
        result["exports_partners"]["partners"] = partners_list

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 14 >>> 'Exports - partners'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'exports_partners_note'
    # "text" - 'exports_partners'
    # --------------------------------------------------------------------------------------------------
    # ['exports_partners', 'exports_partners_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "Canada 16%, Mexico 15%, China 8%, Japan 4%, UK 4% (2022)",
        "note": "<b>note:</b> top five export partners based on percentage share of exports"
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
