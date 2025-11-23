import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_labor_force_by_occupation(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parses labor force data by occupation, extracting percentage and year if available.

    Parameters:
        test_data (dict): The dictionary containing labor force occupation data.

    Returns:
        dict: A dictionary with parsed data for labor force by occupation and year.
    """
    result = {}

    for key, value in test_data.items():
        # Define the base key name based on the occupation
        base_key = f"labor_force_{key.replace(' ', '_').lower()}"

        # Extract the text value
        text = value.get("text", "")

        # Extract percentage and year if available
        match = re.match(r"([\d.]+)%(?: \((\d{4}) est\.\))?", text)
        if match:
            percentage = float(match.group(1))
            year = int(match.group(2)) if match.group(2) else ""
            result[base_key] = {
                "percentage": percentage,
                "year": year
            }
        else:
            logging.warning(
                f"Unexpected format in 'text' data for {key}: {text}")

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 31 >>> 'Labor force - by occupation'
    # --------------------------------------------------------------------------------------------------
    # "agriculture" - 'labor_force_agriculture'
    # "industry" - 'labor_force_industry'
    # "industry and services" - 'labor_force_industry_services'
    # --------------------------------------------------------------------------------------------------
    # ['labor_force_agriculture', 'labor_force_industry', 'labor_force_industry_services']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "agriculture": {
            "text": "50%"
        },
        "industry": {
            "text": "50%"
        },
        "industry and services": {
            "text": "50% (2005 est.)"
        }
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
