import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


# Key mapping dictionary for clear output structure
KEY_MAPPING = {
    "agriculture": "gdp_agriculture",
    "industry": "gdp_industry",
    "services": "gdp_services"
}


def parse_gdp_composition_sector_of_origin(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """
    Parses GDP composition by sector of origin data including values, dates, and notes.

    Parameters:
        test_data (dict): The dictionary containing GDP composition data by sector.

    Returns:
        dict: A dictionary with parsed GDP composition data by sector.
    """
    if return_original:
        return test_data

    result = {}

    # Handle each GDP composition sector
    for key, mapped_key in KEY_MAPPING.items():
        data = test_data.get(key, {})
        text = data.get("text", "")
        if text:
            # Extract value and year
            match = re.match(r"(-?[\d.]+)%\s+\((\d{4})", text)
            if match:
                result[mapped_key] = {
                    "value": float(match.group(1)),
                    "unit": "%",
                    "year": int(match.group(2))
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' field if it exists
    if "note" in test_data:
        result["gdp_composition_note"] = clean_text(test_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 19 >>> 'GDP - composition, by sector of origin'
    # --------------------------------------------------------------------------------------------------
    # "agriculture" - 'gdp_composition_agriculture'
    # "industry" - 'gdp_composition_industry'
    # "note" - 'gdp_composition_note'
    # "services" - 'gdp_composition_services'
    # --------------------------------------------------------------------------------------------------
    # ['gdp_composition_agriculture', 'gdp_composition_industry', 'gdp_composition_note', 'gdp_composition_services']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "agriculture": {
            "text": "0.9% (2017 est.)"
        },
        "industry": {
            "text": "19.1% (2017 est.)"
        },
        "services": {
            "text": "80% (2017 est.)"
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
