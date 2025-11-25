import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_reserves_of_foreign_exchange_and_gold(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """
    Parses reserves of foreign exchange and gold data, extracting the value, unit, and year.

    Parameters:
        test_data (dict): The dictionary containing reserves data.

    Returns:
        dict: A dictionary with parsed data for reserves of foreign exchange and gold.
    """
    if return_original:
        return test_data

    result = {}

    for key, value in test_data.items():
        if key == "note":
            # Process 'note' field
            result["reserves_note"] = clean_text(value)
        else:
            # Extract the year from the key
            year_match = re.search(r'\d{4}', key)
            if not year_match:
                logging.warning(f"No year found in key: {key}")
                continue

            year = year_match.group(0)

            # Process 'text' field for value and unit
            text = value.get("text", "")
            match = re.match(r"\$(\d[\d,.]*)\s*(\w+)\s*\((\d{4})", text)
            if match:
                value_num = float(match.group(1).replace(",", ""))
                unit = match.group(2)
                result[f"reserves_{year}"] = {
                    "value": value_num,
                    "unit": unit,
                    "year": int(year)
                }
            else:
                logging.warning(f"Unexpected format in 'text' data: {text}")

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 38 >>> 'Reserves of foreign exchange and gold'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    test_data = {
        "Reserves of foreign exchange and gold 2023": {
            "text": "$4.756 billion (2023 est.)"
        },
        "Reserves of foreign exchange and gold 2022": {
            "text": "$4.279 billion (2022 est.)"
        },
        "Reserves of foreign exchange and gold 2021": {
            "text": "$4.802 billion (2021 est.)"
        },
        "note": "<b>note:</b> holdings of gold (year-end prices)/foreign exchange/special drawing rights in current dollars"
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
