'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF MILITARY INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_military ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.get_military import get_military
from proj_004_cia.c_00_transform_utils.clean_output import clean_output
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_military_data(
    data: dict,
    iso3Code: str
):

    # 10. MILITARY
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # WORLD-SPECIFIC: Use comprehensive World parser
    if iso3Code == 'WLD':
        cia_pack['world_military'] = get_military(
            data=data, info='world_military', iso3Code=iso3Code)
        return clean_output(cia_pack)

    # Note: 'military_note'
    cia_pack['military_note'] = get_military(
        data=data, info='military_note', iso3Code=iso3Code)
    # Note: 'military_forces'
    cia_pack['military_forces'] = get_military(
        data=data, info='military_forces', iso3Code=iso3Code)
    # Note: 'military_personnel'
    cia_pack['military_personnel'] = get_military(
        data=data, info='military_personnel', iso3Code=iso3Code)
    # Note: 'deployments'
    cia_pack['deployments'] = get_military(
        data=data, info='deployments', iso3Code=iso3Code)
    # Note: 'military_inventories'
    cia_pack['military_inventories'] = get_military(
        data=data, info='military_inventories', iso3Code=iso3Code)
    # Note: 'military_expenditures'
    cia_pack['military_expenditures'] = get_military(
        data=data, info='military_expenditures', iso3Code=iso3Code)
    # Note: 'military_age'
    cia_pack['military_age'] = get_military(
        data=data, info='military_age', iso3Code=iso3Code)

    # Return the compiled geography data
    return clean_output(cia_pack)


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
    pprint(return_military_data(data=data, iso3Code=iso3Code))
