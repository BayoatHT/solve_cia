import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_youth_unemployment_rate(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parses youth unemployment data for total, male, and female categories, extracting
    the unemployment percentage and year, and processing notes if available.

    Parameters:
        test_data (dict): The dictionary containing youth unemployment data.

    Returns:
        dict: A dictionary with parsed youth unemployment data.
    """
    result = {}

    # Define keys to process
    categories = {
        "total": "youth_unemployment_total",
        "male": "youth_unemployment_male",
        "female": "youth_unemployment_female"
    }

    # Parse each category
    for key, result_key in categories.items():
        if key in test_data:
            text = test_data[key].get("text", "")
            match = re.match(r"([\d.]+)%\s*\((\d{4})", text)
            if match:
                result[result_key] = {
                    "value": float(match.group(1)),
                    "year": int(match.group(2))
                }
            else:
                app_logger.warning(
                    f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' if present
    if "note" in test_data:
        result["youth_unemployment_note"] = clean_text(test_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "female" - 'youth_unemployment_female'
    # "male" - 'youth_unemployment_male'
    # "note" - 'youth_unemployment_note'
    # "total" - 'youth_unemployment_total'
    # --------------------------------------------------------------------------------------------------
    # ['youth_unemployment_female', 'youth_unemployment_male', 'youth_unemployment_note', 'youth_unemployment_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "total": {
            "text": "45.4% (2023 est.)"
        },
        "male": {
            "text": "40.5% (2023 est.)"
        },
        "female": {
            "text": "51.5% (2023 est.)"
        },
        "note": "<b>note:</b> % of labor force ages 15-24 seeking employment"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = None
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
    test_youth_unemployment_rate_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Admin Divisions Orginal Data")
    for index, country_data in enumerate(test_youth_unemployment_rate_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing youth_unemployment_rate Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_youth_unemployment_rate_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_youth_unemployment_rate(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
