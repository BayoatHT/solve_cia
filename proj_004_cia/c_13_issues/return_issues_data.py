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
        return_issues_data(
            data=data,
            iso3Code=iso3Code
        )
    )
