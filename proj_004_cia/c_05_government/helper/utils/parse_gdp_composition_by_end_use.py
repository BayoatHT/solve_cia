import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------

# Key mapping dictionary for clear output structure
KEY_MAPPING = {
    "exports of goods and services": "gdp_exports",
    "government consumption": "gdp_govt_consumption",
    "household consumption": "gdp_household_consumption",
    "imports of goods and services": "gdp_imports",
    "investment in fixed capital": "gdp_investment_fixed_capital",
    "investment in inventories": "gdp_investment_inventories"
}


def parse_gdp_composition_by_end_use(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parses GDP composition by end use data including values, dates, and notes.

    Parameters:
        test_data (dict): The dictionary containing GDP composition data.

    Returns:
        dict: A dictionary with parsed GDP composition data by end use.
    """
    result = {}

    # Handle each GDP composition category
    for key, mapped_key in KEY_MAPPING.items():
        data = test_data.get(key, {})
        text = data.get("text", "")
        if text:
            # Extract value and year
            value_match = re.match(r"(-?[\d.]+)%\s+\((\d{4})", text)
            if value_match:
                result[mapped_key] = {
                    "value": float(value_match.group(1)),
                    "unit": "%",
                    "year": int(value_match.group(2))
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' field if it exists
    if "note" in test_data:
        result["gdp_composition_note"] = clean_text(test_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 18 >>> 'GDP - composition, by end use'
    # --------------------------------------------------------------------------------------------------
    # "exports of goods and services" - 'gdp_composition_exports'
    # "government consumption" - 'gdp_composition_govt_consumption'
    # "household consumption" - 'gdp_composition_household_consumption'
    # "imports of goods and services" - 'gdp_composition_imports'
    # "investment in fixed capital" - 'gdp_composition_investment_fixed_capital'
    # "investment in inventories" - 'gdp_composition_investment_inventories'
    # "note" - 'gdp_composition_note'
    # --------------------------------------------------------------------------------------------------
    # ['gdp_composition_exports', 'gdp_composition_govt_consumption', 'gdp_composition_household_consumption',
    # 'gdp_composition_imports', 'gdp_composition_investment_fixed_capital', 'gdp_composition_investment_inventories',
    # 'gdp_composition_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "household consumption": {
            "text": "68.4% (2017 est.)"
        },
        "government consumption": {
            "text": "17.3% (2017 est.)"
        },
        "investment in fixed capital": {
            "text": "17.2% (2017 est.)"
        },
        "investment in inventories": {
            "text": "0.1% (2017 est.)"
        },
        "exports of goods and services": {
            "text": "12.1% (2017 est.)"
        },
        "imports of goods and services": {
            "text": "-15% (2017 est.)"
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
