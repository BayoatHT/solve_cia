import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_remittances(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """
    Parses remittance data, extracting the percentage of GDP and year from each entry.

    Parameters:
        test_data (dict): The dictionary containing remittance data.

    Returns:
        dict: A dictionary with parsed data for remittances by year and additional notes.
    """
    if return_original:
        return test_data

    result = {}

    for key, value in test_data.items():
        if key == "note":
            # Process 'note' field
            result["remittances_note"] = clean_text(value)
        else:
            # Extract the year from the key
            year_match = re.search(r'\d{4}', key)
            if not year_match:
                logging.warning(f"No year found in key: {key}")
                continue

            year = year_match.group(0)

            # Process 'text' field for percentage and year
            text = value.get("text", "")
            match = re.match(r"([\d.]+)% of GDP \((\d{4})", text)
            if match:
                percentage = float(match.group(1))
                result[f"remittances_{year}"] = {
                    "percentage_of_gdp": percentage,
                    "year": int(year)
                }
            else:
                logging.warning(f"Unexpected format in 'text' data: {text}")

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 37 >>> 'Remittances'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    test_data = {
        "Remittances 2023": {
            "text": "0.31% of GDP (2023 est.)"
        },
        "Remittances 2022": {
            "text": "0.34% of GDP (2022 est.)"
        },
        "Remittances 2021": {
            "text": "0.32% of GDP (2021 est.)"
        },
        "note": "<b>note:</b> personal transfers and compensation between resident and non-resident individuals/households/entities"
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
