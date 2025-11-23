import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_member_states(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note" - 'member_states_note',
    # "text" - 'member_states',
    # --------------------------------------------------------------------------------------------------
    # ['member_states_note', 'member_states']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "<p>27 countries: Austria, Belgium, Bulgaria, Croatia, Cyprus, Czechia, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden; note - 9 candidate countries: Albania, Bosnia and Herzegovina, Georgia, Moldova, Montenegro, North Macedonia, Serbia, Turkey, Ukraine</p> <p>there are 13 overseas countries and territories (OCTs) (1 with Denmark [Greenland], 6 with France [French Polynesia, French Southern and Antarctic Lands, New Caledonia, Saint Barthelemy, Saint Pierre and Miquelon, Wallis and Futuna], and 6 with the Netherlands [Aruba, Bonaire, Curacao, Saba, Sint Eustatius, Sint Maarten]), all are part of the Overseas Countries and Territories Association (OCTA)</p>",
        "note": "<strong>note:</strong> there are non-European OCTs having special relations with Denmark, France, and the Netherlands (list is annexed to the Treaty on the Functioning of the European Union), that are associated with the EU to promote their economic and social development; member states apply to their trade with OCTs the same treatment as they accord each other pursuant to the treaties; OCT nationals are in principle EU citizens, but these countries are neither part of the EU, nor subject to the EU"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Member states'
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
    test_member_states_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Member states Orginal Data")
    for index, country_data in enumerate(test_member_states_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing member_states Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_member_states_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_member_states(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
