import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_agricultural_products(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parses agricultural products information, extracting date, products, and note (if available).

    Parameters:
        test_data (dict): The dictionary containing agricultural products data.

    Returns:
        dict: Parsed agricultural products with keys `date`, `agricultural_products`, and `agricultural_products_note`.
    """
    result = {
        "agricultural_products": [],
        "date": "",
        "agricultural_products_note": ""
    }

    # Extract text for products and note, if available
    text = test_data.get("text", "")
    note = test_data.get("note", "")

    # Check if the text ends with a date in parentheses and extract it
    date_match = re.search(r"\((\d{4})\)$", text)
    if date_match:
        result["date"] = date_match.group(1)
        # Remove the date portion from the text
        text = text[:date_match.start()].strip()

    # Split the text by commas for agricultural products
    result["agricultural_products"] = [item.strip()
                                       for item in text.split(",")]

    # Clean the note text if present
    if note:
        result["agricultural_products_note"] = clean_text(note)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 1 >>> 'Agricultural products'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'agricultural_products_note'
    # "text" - 'agricultural_products'
    # --------------------------------------------------------------------------------------------------
    # ['agricultural_products', 'agricultural_products_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "maize, soybeans, milk, wheat, sugarcane, sugar beets, chicken, potatoes, beef, pork (2022)",
        "note": "<b>note:</b> top ten agricultural products based on tonnage"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Agricultural Products'
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
    test_agricultural_products_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Admin Divisions Orginal Data")
    for index, country_data in enumerate(test_agricultural_products_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "50 states and 1 district*; Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, District of Columbia*, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming",
        "note": ""
    }
    parsed_data = parse_agricultural_products(test_data)
    print(parsed_data)
    print("Testing Administrative Divisions Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_agricultural_products_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_agricultural_products(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            assert "agricultural_products" in result
            assert "agricultural_products_note" in result
            print("✅ Structure validation passed")
