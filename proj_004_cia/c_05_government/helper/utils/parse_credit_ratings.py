import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_credit_ratings(test_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses credit ratings data into a structured nested dictionary format.

    Parameters:
        test_data (dict): The dictionary containing credit ratings data.

    Returns:
        dict: A nested dictionary with parsed credit ratings information.
    """
    if return_original:
        return test_data

    result = {
        "credit_ratings_note": "",
        "credit_fitch_rating": {},
        "credit_moodys_rating": {},
        "credit_standard_poor_rating": {}
    }

    # Parse the note if present
    result["credit_ratings_note"] = clean_text(test_data.get("note", ""))

    # Helper function to parse rating and year from text
    def parse_rating(text: str, return_original: bool = False)-> dict:
        if return_original:
            return text

        match = re.match(r"([A-Za-z+]+)\s*\((\d{4})\)", text)
        if match:
            return {
                "rating": match.group(1),
                "year": int(match.group(2))
            }
        return {"rating": "", "year": 0}

    # Parse each rating if present
    if "Fitch rating" in test_data:
        result["credit_fitch_rating"] = parse_rating(
            test_data["Fitch rating"].get("text", ""))
    if "Moody's rating" in test_data:
        result["credit_moodys_rating"] = parse_rating(
            test_data["Moody's rating"].get("text", ""))
    if "Standard & Poors rating" in test_data:
        result["credit_standard_poor_rating"] = parse_rating(
            test_data["Standard & Poors rating"].get("text", ""))

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 6 >>> 'Credit ratings'
    # --------------------------------------------------------------------------------------------------
    # "Fitch rating" - 'credit_fitch_rating'
    # "Moody's rating" - 'credit_moodys_rating'
    # "Standard & Poors rating" - 'credit_standard_poor_rating'
    # "note" - 'credit_ratings_note'
    # --------------------------------------------------------------------------------------------------
    # ['credit_fitch_rating', 'credit_moodys_rating', 'credit_standard_poor_rating', 'credit_ratings_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "Fitch rating": {
            "text": "AAA (1994)"
        },
        "Moody's rating": {
            "text": "Aaa (1949)"
        },
        "Standard & Poors rating": {
            "text": "AA+ (2011)"
        },
        "note": "<strong>note: </strong>The year refers to the year in which the current credit rating was first obtained."
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
