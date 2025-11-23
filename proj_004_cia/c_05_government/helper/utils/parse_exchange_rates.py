import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_exchange_rates(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 11 >>> 'Exchange rates'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "<strong>British pounds per US dollar: </strong>0.805 (2023 est.), 0.811 (2022 est.), 0.727 (2021 est.), 0.780 (2020 est.), 0.783 (2019 est.)<br><strong>Canadian dollars per US dollar: </strong>1.35 (2023 est.), 1.302 (2022 est.), 1.254 (2021 est.), 1.341 (2020 est.), 1.327 (2019 est.)<br><strong>Chinese yuan per US dollar: </strong>7.084 (2023 est.), 6.737 (2022 est.), 6.449 (2021 est.), 6.901 (2020 est.), 6.908 (2019 est.)<br><strong>euros per US dollar: </strong>0.925 (2023 est.), 0.950 (2022 est.), 0.845 (2021 est.), 0.876 (2020 est.), 0.893 (2019 est.)<br><strong>Japanese yen per US dollar: </strong>140.49 (2023 est.), 131.50 (2022 est.), 109.75 (2021 est.), 106.78 (2020 est.), 109.01 (2019 est.)<br><br><strong>note 1: </strong>the following countries and territories use the US dollar officially as their legal tender: British Virgin Islands, Ecuador, El Salvador, Marshall Islands, Micronesia, Palau, Timor Leste, Turks and Caicos, and islands of the Caribbean Netherlands (Bonaire, Sint Eustatius, and Saba)<br><br><strong>note 2: </strong>the following countries and territories use the US dollar as official legal tender alongside local currency: Bahamas, Barbados, Belize, Costa Rica, and Panama<br><br><strong>note 3: </strong>the following countries and territories widely accept the US dollar as a dominant currency but have yet to declare it as legal tender: Bermuda, Burma, Cambodia, Cayman Islands, Honduras, Nicaragua, and Somalia"
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
