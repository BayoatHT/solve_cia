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
        return cia_pack

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
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    import platform
    country = True
    # ----------------------------------------------------------------------------------------------------------------------------------
    if platform.system() == 'Windows':
        json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    else:
        json_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_raw_data')
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
        return_military_data(
            data=data,
            iso3Code=iso3Code
        )
    )
