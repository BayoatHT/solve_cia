######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import json
import logging
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.c_00_transform_utils.extract_and_parse import extract_and_parse
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.c_13_issues.helper.utils.parse_displaced_persons import parse_displaced_persons
from proj_004_cia.c_13_issues.helper.utils.parse_illicit_drugs import parse_illicit_drugs
from proj_004_cia.c_13_issues.helper.utils.parse_international import parse_international
from proj_004_cia.c_13_issues.helper.utils.parse_trafficking import parse_trafficking
from proj_004_cia.c_13_issues.helper.utils.parse_issues_world import parse_issues_world


def get_issues(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: Transnational Issues DATA
    # --------------------------------------------------------------------------------------------------
    issues_data = data.get("Transnational Issues", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WORLD-SPECIFIC: Return all issues in one comprehensive dict
    if info == 'world_issues' and iso3Code == 'WLD':
        return parse_issues_world(issues_data, iso3Code)

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    international_data = issues_data.get("Disputes - international", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'international_issues':
        return extract_and_parse(
            main_data=issues_data,
            key_path="Disputes - international",
            parser_function=parse_international,
            iso3Code=iso3Code,
            parser_name="parse_international"
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    drugs_data = issues_data.get("Illicit drugs", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'illicit_drugs':
        return extract_and_parse(
            main_data=issues_data,
            key_path="Illicit drugs",
            parser_function=parse_illicit_drugs,
            iso3Code=iso3Code,
            parser_name="parse_illicit_drugs"
        )

    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    displaced_data = issues_data.get(
        "Refugees and internally displaced persons", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'displaced_persons':
        return extract_and_parse(
            main_data=issues_data,
            key_path="Refugees and internally displaced persons",
            parser_function=parse_displaced_persons,
            iso3Code=iso3Code,
            parser_name="parse_displaced_persons"
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    traffick_data = issues_data.get("Trafficking in persons", {})
    # --------------------------------------------------------------------------------------------------
    # ['trafficked']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'trafficking':
        return extract_and_parse(
            main_data=issues_data,
            key_path="Trafficking in persons",
            parser_function=parse_trafficking,
            iso3Code=iso3Code,
            parser_name="parse_trafficking"
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    from pprint import pprint
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    # --------------------------------------------------------------------------------------------------
    info = 'pass'  # Change this to test specific fields
    iso3Code = 'USA'  # Change to any ISO3 code: 'USA', 'FRA', 'WLD', 'DEU', etc.
    # --------------------------------------------------------------------------------------------------
    data = load_country_data(iso3Code)
    # --------------------------------------------------------------------------------------------------
    pprint(get_issues(data=data, info=info, iso3Code=iso3Code))
