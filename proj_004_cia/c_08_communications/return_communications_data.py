'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF GEOGRAPHY INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_communications ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.get_communications import get_communications

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

    # Conditional inclusion based on iso3Code
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

    # Return the compiled geography data
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    country = False
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = f'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia/_raw_data'
    if country:
        region_folder = f'north-america'
        cia_code = 'us'
    else:
        region_folder = f'world'
        cia_code = 'xx'
    file_path = os.path.join(json_folder, region_folder, f'{cia_code}.json')
    # --------------------------------------------------------------------------------------------------
    with open(file_path, 'r', encoding='utf-8') as country_file:
        data = json.load(country_file)
    # --------------------------------------------------------------------------------------------------
    if country:
        iso3Code = 'USA'
    else:
        iso3Code = 'WLD'
    # ------------------------------------------------------------------------------------------------------------------
    print(
        return_communications_data(
            data=data,
            iso3Code=iso3Code
        )
    )
