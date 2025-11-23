import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._save_test_data_as_text import save_test_data_as_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_citizenship(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parse citizenship data from CIA Government section.

    Args:
        test_data: Dictionary containing citizenship data
        iso3Code: ISO3 country code

    Returns:
        Dictionary with parsed citizenship information
    """
    result = {}

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        field_mappings = {
            'citizenship by birth': 'citizenship_by_birth',
            'citizenship by descent only': 'citizenship_by_descent',
            'dual citizenship recognized': 'dual_citizenship_recognized',
            'residency requirement for naturalization': 'residency_requirement',
        }

        for cia_key, output_key in field_mappings.items():
            if cia_key in test_data:
                field_data = test_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
                elif isinstance(field_data, str) and field_data.strip():
                    result[output_key] = clean_text(field_data)

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['citizenship_note'] = clean_text(note)

    except Exception as e:
        app_logger.error(f"Error parsing citizenship: {e}")

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "citizenship by birth" - 'citizen_by_birth'
    # "citizenship by descent only" - 'citizen_by_descent'
    # "dual citizenship recognized" - 'dual_citizenship'
    # "note" - 'citizenship_note'
    # "residency requirement for naturalization" - 'residency_req'
    # --------------------------------------------------------------------------------------------------
    # ['citizen_by_birth', 'citizen_by_descent', 'dual_citizenship', 'citizenship_note', 'residency_req']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "citizenship by birth": {
            "text": "yes"
        },
        "citizenship by descent only": {
            "text": "yes"
        },
        "dual citizenship recognized": {
            "text": "no, but the US government acknowledges such situtations exist; US citizens are not encouraged to seek dual citizenship since it limits protection by the US"
        },
        "residency requirement for naturalization": {
            "text": "5 years"
        }
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Citizenship'
    # --------------------------------------------------------------------------------------------------
    # List of countries to test
    test_countries = [
        'EEU', 'WLD', 'DZA', 'AGO', 'BWA', 'BEN', 'BDI', 'TCD', 'COG', 'COD', 'CMR',
        'COM', 'CAF', 'CPV', 'DJI', 'EGY', 'GNQ', 'ERI', 'ETH', 'GMB', 'GAB', 'GHA',
        'GIN', 'CIV', 'KEN', 'LBR', 'LSO', 'LBY', 'MDG', 'MWI', 'MLI', 'MAR', 'MUS',
        'MRT', 'MOZ', 'NER', 'NGA', 'SSD', 'GNB', 'RWA', 'SYC', 'ZAF', 'SEN', 'SHN',
        'SLE', 'SOM', 'SDN', 'TGO', 'STP', 'TUN', 'TZA', 'UGA', 'BFA', 'NAM', 'ESH',
        'SWZ', 'ZMB', 'ZWE', 'ASM', 'AUS', 'ATC', 'SLB', 'CCK', 'MNP', 'CSI', 'COK',
        'FJI', 'FSM', 'PYF', 'GUM', 'KIR', 'CXR', 'NCL', 'NIU', 'NFK', 'VUT', 'NRU',
        'NZL', 'PCN', 'PLW', 'MHL', 'TKL', 'TON', 'TUV', 'UMI', 'WLF', 'PGA', 'WSM',
        'ABW', 'ATG', 'AIA', 'BRB', 'BHS', 'BLZ', '', 'CYM', 'CRI', 'CUB', 'DMA',
        'DOM', 'SLV', 'GRD', 'GTM', 'HTI', 'HND', 'JAM', 'MSR', 'SXM', 'NIC', 'PAN',
        'MAF', 'PRI', 'KNA', 'LCA', 'BLM', 'TTO', 'TCA', 'CUW', 'VCT', 'VGB', 'VIR',
        'KGZ', 'KAZ', 'RUS', 'TJK', 'TKM', 'UZB', 'MMR', 'BRN', 'KHM', 'CHN', 'HKG',
        'IDN', 'JPN', 'PRK', 'KOR', 'LAO', 'MAC', 'MNG', 'MYS', 'XPI', 'XSP', 'PNG',
        'PHL', 'SGP', 'THA', 'TLS', 'TWN', 'VNM', 'ALB', 'AND', 'AUT', '',
        'BEL', 'BIH', 'BLR', 'BGR', 'CYP', 'DNK', '', 'IRL', 'EST', 'CZE', 'FIN',
        'FRO', 'FRA', 'GIB', 'GGY', 'DEU', 'GRC', 'HRV', 'HUN', 'ISL', 'IMN', 'ITA',
        'JEY', '', 'XKX', 'LVA', 'LTU', 'SVK', 'LIE', 'LUX', 'MDA', 'MNE', 'MKD', 'MCO',
        'MLT', 'NLD', 'NOR', 'POL', 'PRT', 'SRB', 'ROU', 'SVN', 'SMR', 'ESP', '', 'SWE',
        'CHE', 'GBR', 'UKR', 'VAT', 'ARE', 'AZE', 'ARM', 'BHR', 'GEO', '', 'IRN', 'ISR',
        'IRQ', 'JOR', 'KWT', 'LBN', 'OMN', 'QAT', 'SAU', 'SYR', 'TUR', '', 'YEM', 'BMU',
        'CAN', 'GRL', 'XCL', 'MEX', 'SPM', 'USA', 'ARG', 'BOL', 'BRA', 'CHL', 'COL', 'ECU',
        'FLK', 'GUY', 'SUR', 'PRY', 'PER', 'SGS', 'URY', 'VEN', 'AFG', 'BGD', 'BTN', 'LKA',
        'IND', 'IOT', 'MDV', 'NPL', 'PAK']
    # --------------------------------------------------------------------------------------------------

    test_capital_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=300
    )

    print(f"Test Citizenship Orginal Data")
    # --------------------------------------------------------------------------------------------------
    test_folder = 'C:\\Users\\bayoa\\impact_projects\\claude_solve_cia\\proj_004_cia\\c_05_government\\helper\\_test_files'
    # Save the test data to a file for inspection - .txt
    file_name = "Capital"
    file_path = save_test_data_as_text(
        test_data=test_capital_data,
        test_folder=test_folder,
        file_name=file_name
    )

    """
    for index, country_data in enumerate(test_admin_divisions_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    """
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    test_data = {
        "text": "50 states and 1 district*; Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware, District of Columbia*, Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana, Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana, Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina, North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina, South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia, Wisconsin, Wyoming",
        "note": ""
    }
    parsed_data = parse_citizenship(test_data)
    print(parsed_data)
    print("Testing Citizenship Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_capital_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_citizenship(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
