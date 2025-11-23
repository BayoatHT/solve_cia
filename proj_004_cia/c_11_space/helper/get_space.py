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
    from pprint import pprint
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    # --------------------------------------------------------------------------------------------------
    info = 'pass'  # Change this to test specific fields
    iso3Code = 'USA'  # Change to any ISO3 code: 'USA', 'FRA', 'WLD', 'DEU', etc.
    # --------------------------------------------------------------------------------------------------
    data = load_country_data(iso3Code)
    # --------------------------------------------------------------------------------------------------
    pprint(get_space(data=data, info=info, iso3Code=iso3Code))
