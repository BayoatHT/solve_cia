import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_unemployment_rate(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parses the unemployment rate data, extracting values and years for each entry and handling notes.

    Parameters:
        test_data (dict): The dictionary containing unemployment rate data.

    Returns:
        dict: A dictionary with parsed unemployment rate data by year and any associated notes.
    """
    result = {}

    # Process each key in test_data
    for key, data in test_data.items():
        # Match keys that contain a year
        year_match = re.search(r"(\d{4})", key)
        if year_match:
            year = year_match.group(1)
            text = data.get("text", "")
            # Extract value and year from text
            match = re.match(r"([\d.]+)%\s*\((\d{4})", text)
            if match:
                result[f"unemploy_rate_{year}"] = {
                    "value": float(match.group(1)),
                    "year": int(match.group(2))
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")
        elif key == "note":
            data = data.replace("note:", "")
            # Handle 'note' key
            result["unemploy_rate_note"] = clean_text(data)

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Unemployment rate 2014" - 'unemploy_rate_2014'
    # "Unemployment rate 2015" - 'unemploy_rate_2015'
    # "Unemployment rate 2016" - 'unemploy_rate_2016'
    # "Unemployment rate 2017" - 'unemploy_rate_2017'
    # "Unemployment rate 2018" - 'unemploy_rate_2018'
    # "Unemployment rate 2019" - 'unemploy_rate_2019'
    # "Unemployment rate 2020" - 'unemploy_rate_2020'
    # "Unemployment rate 2021" - 'unemploy_rate_2021'
    # "Unemployment rate 2022" - 'unemploy_rate_2022'
    # "Unemployment rate 2023" - 'unemploy_rate_2023'
    # "note" - 'unemploy_rate_note'
    # --------------------------------------------------------------------------------------------------
    # ['unemploy_rate_2014', 'unemploy_rate_2015', 'unemploy_rate_2016', 'unemploy_rate_2017',
    # 'unemploy_rate_2018', 'unemploy_rate_2019', 'unemploy_rate_2020', 'unemploy_rate_2021',
    # 'unemploy_rate_2022', 'unemploy_rate_2023', 'unemploy_rate_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "Unemployment rate 2023": {
            "text": "23.38% (2023 est.)"
        },
        "Unemployment rate 2022": {
            "text": "23.62% (2022 est.)"
        },
        "Unemployment rate 2021": {
            "text": "23.11% (2021 est.)"
        },
        "note": "<b>note:</b> % of labor force seeking employment"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'unemployment_rate'
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
    test_unemployment_rate_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Admin Divisions Orginal Data")
    for index, country_data in enumerate(test_unemployment_rate_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing unemployment_rate Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_unemployment_rate_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_unemployment_rate(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
