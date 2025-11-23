'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF COMMUNICATIONS INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_communications ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.get_communications import get_communications
from proj_004_cia.c_00_transform_utils.clean_output import clean_output

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_communications_data(
    data: dict,
    iso3Code: str
):

    # 8. COMMUNICATIONS
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # WORLD-SPECIFIC: Use comprehensive World parser
    if iso3Code == 'WLD':
        cia_pack['world_communications'] = get_communications(
            data=data, info='world_communications', iso3Code=iso3Code)
        return clean_output(cia_pack)

    # Conditional inclusion for individual countries
    if iso3Code != 'WLD':
        # Note: 'broadband_fixed'
        cia_pack['broadband_fixed'] = get_communications(
            data=data, info='broadband_fixed', iso3Code=iso3Code)
        # Note: 'broadband_media'
        cia_pack['broadband_media'] = get_communications(
            data=data, info='broadband_media', iso3Code=iso3Code)
        # Note: 'communications_note'
        cia_pack['communications_note'] = get_communications(
            data=data, info='communications_note', iso3Code=iso3Code)
        # Note: 'internet_code'
        cia_pack['internet_code'] = get_communications(
            data=data, info='internet_code', iso3Code=iso3Code)
        # Note: 'internet_users'
        cia_pack['internet_users'] = get_communications(
            data=data, info='internet_users', iso3Code=iso3Code)
        # Note: 'tele_systems'
        cia_pack['tele_systems'] = get_communications(
            data=data, info='tele_systems', iso3Code=iso3Code)
        # Note: 'phone_fixed_lines'
        cia_pack['phone_fixed_lines'] = get_communications(
            data=data, info='phone_fixed_lines', iso3Code=iso3Code)
        # Note: 'phone_mobile_cellular'
        cia_pack['phone_mobile_cellular'] = get_communications(
            data=data, info='phone_mobile_cellular', iso3Code=iso3Code)
    else:
        # Note: ''
        pass

    # Return the compiled communications data
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
    pprint(return_communications_data(data=data, iso3Code=iso3Code))
