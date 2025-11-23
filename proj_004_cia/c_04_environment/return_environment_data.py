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
from pprint import pprint
# get_environment ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_04_environment.helper.get_environment import get_environment

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_environment_data(
    data: dict,
    iso3Code: str
):

    # 4. ENVIRONMENT
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # Note: 'air_pollutants'
    cia_pack['air_pollutants'] = get_environment(
        data=data, info='air_pollutants', iso3Code=iso3Code)
    # Note: 'climate'
    cia_pack['climate'] = get_environment(
        data=data, info='climate', iso3Code=iso3Code)
    # Note: 'env_current_issues'
    cia_pack['env_current_issues'] = get_environment(
        data=data, info='env_current_issues', iso3Code=iso3Code)
    # Note: 'env_international_agreements'
    cia_pack['env_international_agreements'] = get_environment(
        data=data, info='env_international_agreements', iso3Code=iso3Code)
    # Note: 'food_insecurity'
    cia_pack['food_insecurity'] = get_environment(
        data=data, info='food_insecurity', iso3Code=iso3Code)
    # Note: 'geoparks'
    cia_pack['geoparks'] = get_environment(
        data=data, info='geoparks', iso3Code=iso3Code)
    # Note: 'land_use'
    cia_pack['land_use'] = get_environment(
        data=data, info='land_use', iso3Code=iso3Code)
    # Note: 'major_aquifers'
    cia_pack['major_aquifers'] = get_environment(
        data=data, info='major_aquifers', iso3Code=iso3Code)
    # Note: 'major_lakes'
    cia_pack['major_lakes'] = get_environment(
        data=data, info='major_lakes', iso3Code=iso3Code)
    # Note: 'major_rivers'
    cia_pack['major_rivers'] = get_environment(
        data=data, info='major_rivers', iso3Code=iso3Code)
    # Note: 'major_watersheds'
    cia_pack['major_watersheds'] = get_environment(
        data=data, info='major_watersheds', iso3Code=iso3Code)
    # Note: 'revenue_from_coal'
    cia_pack['revenue_from_coal'] = get_environment(
        data=data, info='revenue_from_coal', iso3Code=iso3Code)
    # Note: 'revenue_from_forest'
    cia_pack['revenue_from_forest'] = get_environment(
        data=data, info='revenue_from_forest', iso3Code=iso3Code)
    # Note: 'total_renewable_water'
    cia_pack['total_renewable_water'] = get_environment(
        data=data, info='total_renewable_water', iso3Code=iso3Code)
    # Note: 'total_water_withdrawal'
    cia_pack['total_water_withdrawal'] = get_environment(
        data=data, info='total_water_withdrawal', iso3Code=iso3Code)
    # Note: 'urbanization'
    cia_pack['urbanization'] = get_environment(
        data=data, info='urbanization', iso3Code=iso3Code)
    # Note: 'waste_and_recycling'
    cia_pack['waste_and_recycling'] = get_environment(
        data=data, info='waste_and_recycling', iso3Code=iso3Code)
    # Note: 'world_biomes'
    cia_pack['world_biomes'] = get_environment(
        data=data, info='world_biomes', iso3Code=iso3Code)
    # Note: 'marine_fisheries'
    cia_pack['marine_fisheries'] = get_environment(
        data=data, info='marine_fisheries', iso3Code=iso3Code)

    # Return the compiled environment data
    return cia_pack
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # ------------------------------------------------------------------------------------------------------------------
    # RETURN
    # ------------------------------------------------------------------------------------------------------------------
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    country = True
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
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
    pprint(
        return_environment_data(
            data=data,
            iso3Code=iso3Code
        )
    )
