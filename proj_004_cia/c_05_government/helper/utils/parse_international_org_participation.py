import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_international_org_participation(
    test_data: dict,
    iso3Code: str = None
, return_original: bool = False)-> dict:
    """Parse international org participation from CIA Government section."""
    if return_original:
        return test_data

    result = {}
    if not test_data or not isinstance(test_data, dict):
        return result
    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['international_org_participation'] = clean_text(text)
        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['international_org_participation_note'] = clean_text(note)
    except Exception as e:
        app_logger.error(f"Error parsing international_org_participation: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "note", - 'intl_org_participation_note'
    # "text" - 'intl_org_participation'
    # --------------------------------------------------------------------------------------------------
    # ['intl_org_participation_note', 'intl_org_participation']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    test_data = {
        "text": "ADB (nonregional member), AfDB (nonregional member), ANZUS, APEC, Arctic Council, ARF, ASEAN (dialogue partner), Australia Group, BIS, BSEC (observer), CBSS (observer), CD, CE (observer), CERN (observer), CICA (observer), CP, EAPC, EAS, EBRD, EITI (implementing country), FAO, FATF, G-5, G-7, G-8, G-10, G-20, IADB, IAEA, IBRD, ICAO, ICC (national committees), ICRM, IDA, IEA, IFAD, IFC, IFRCS, IGAD (partners), IHO, ILO, IMF, IMO, IMSO, Interpol, IOC, IOM, ISO, ITSO, ITU, ITUC (NGOs), MIGA, MINUSTAH, MONUSCO, NAFTA, NATO, NEA, NSG, OAS, OECD, OPCW, OSCE, Pacific Alliance (observer), Paris Club, PCA, PIF (partner), Quad, SAARC (observer), SELEC (observer), SICA (observer), SPC, UN, UNCTAD, UNESCO, UNHCR, UNHRC, UNITAR, UNMIL, UNMISS, UNOOSA, UNRWA, UN Security Council (permanent), UNTSO, UPU, USMCA, Wassenaar Arrangement, WCO, WHO, WIPO, WMO, WTO, ZC"
    }
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'International organization participation'
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
    test_international_org_participation_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test International organization participation Orginal Data")
    for index, country_data in enumerate(test_international_org_participation_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing international_org_participation Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_international_org_participation_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_international_org_participation(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
