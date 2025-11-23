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
# -----------------------------------------------------------------------------------------------------
from proj_004_cia.c_11_space.helper.utils.parse_space import parse_space
from proj_004_cia.c_11_space.helper.utils.parse_space_world import parse_space_world
# //////////////////////////////////////////////////////////////////////////////////////////////////


def get_space(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: Space DATA
    # --------------------------------------------------------------------------------------------------
    space_data = data.get("Space", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'space':
        # Use World-specific parser for WLD
        if iso3Code == 'WLD':
            return parse_space_world(space_data, iso3Code)

        return extract_and_parse(
            main_data=data,
            key_path="Space",
            parser_function=parse_space,
            iso3Code=iso3Code,
            parser_name="space"
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':

    import platform
    # ---------------------------------------------------------------------------------------------------------------------------------
    info = 'space'
    # ---------------------------------------------------------------------------------------------------------------------------------
    country = "USA"
    # ----------------------------------------------------------------------------------------------------------------------------------
    if platform.system() == 'Windows':
        json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    else:
        json_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '_raw_data')
    if country == "USA":
        region_folder = f'north-america'
        cia_code = 'us'
    elif country == "FRA":
        region_folder = f'europe'
        cia_code = 'fr'
    elif country == "WLD":
        region_folder = f'world'
        cia_code = 'xx'
    file_path = os.path.join(json_folder, region_folder, f'{cia_code}.json')
    # --------------------------------------------------------------------------------------------------
    with open(file_path, 'r', encoding='utf-8') as country_file:
        data = json.load(country_file)
    # --------------------------------------------------------------------------------------------------
    iso3Code = country
    # --------------------------------------------------------------------------------------------------
    from pprint import pprint
    pprint(
        get_space(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
