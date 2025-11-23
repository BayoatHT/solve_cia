'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF TERRORISM INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_issues ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_13_issues.helper.get_issues import get_issues
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_issues_data(
    data: dict,
    iso3Code: str
):

    # 13. ISSUES
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # WORLD-SPECIFIC: Use comprehensive World parser
    if iso3Code == 'WLD':
        cia_pack['world_issues'] = get_issues(
            data=data, info='world_issues', iso3Code=iso3Code)
        return cia_pack

    # Conditional inclusion for individual countries

    # Note: 'international_issues'
    cia_pack['international_issues'] = get_issues(
        data=data, info='international_issues', iso3Code=iso3Code)
    # Note: 'illicit_drugs'
    cia_pack['illicit_drugs'] = get_issues(
        data=data, info='illicit_drugs', iso3Code=iso3Code)
    # Note: 'displaced_persons'
    cia_pack['displaced_persons'] = get_issues(
        data=data, info='displaced_persons', iso3Code=iso3Code)
    # Note: 'trafficking'
    cia_pack['trafficking'] = get_issues(
        data=data, info='trafficking', iso3Code=iso3Code)

    # Return the compiled geography data
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    from pprint import pprint
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    # --------------------------------------------------------------------------------------------------
    iso3Code = 'USA'  # Change to any ISO3 code: 'USA', 'FRA', 'WLD', 'DEU', etc.
    # --------------------------------------------------------------------------------------------------
    data = load_country_data(iso3Code)
    # --------------------------------------------------------------------------------------------------
    pprint(return_issues_data(data=data, iso3Code=iso3Code))
