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
# --------------------------------------------------------------------------------------------------
# NOTE: "Military - note"
# >>> ['mil_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_military_note import parse_military_note
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Military and security forces"
# >>> ['mil_forces', 'mil_forces_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_military_forces import parse_military_forces
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Military and security service personnel strengths"
# >>> ['mil_person', 'mil_person_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_military_personnel import parse_military_personnel
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Military deployments"
# >>> ['mil_deploy', 'mil_deploy_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_deployments import parse_deployments
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Military equipment inventories and acquisitions"
# >>> ['mil_equip', 'mil_equip_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_military_inventories import parse_military_inventories
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Military service age and obligation"
# >>> ['mil_age', 'mil_age_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_military_age import parse_military_age
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Military expenditures"
# >>> ['mil_expend', 'mil_expend_note'] - also has yearly figures but we will use world bank data for that
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_10_military.helper.utils.parse_military_expenditures import parse_military_expenditures
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# #////////////////////////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////////////////////////////////////////


from proj_004_cia.c_10_military.helper.utils.parse_military_world import parse_military_world


def get_military(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: Military and Security DATA
    # --------------------------------------------------------------------------------------------------
    mil_data = data.get("Military and Security", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WORLD-SPECIFIC: Return comprehensive World military data
    if info == 'world_military' and iso3Code == 'WLD':
        return parse_military_world(mil_data, iso3Code)

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'Military - note'
    # --------------------------------------------------------------------------------------------------
    mil_note_data = mil_data.get("Military - note", {})
    # --------------------------------------------------------------------------------------------------
    # ['mil_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'military_note':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military - note",
            parser_function=parse_military_note,
            iso3Code=iso3Code,
            parser_name="parse_military_note"
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'Military and security forces'
    # --------------------------------------------------------------------------------------------------
    military_security_forces_data = mil_data.get(
        "Military and security forces", {})
    # --------------------------------------------------------------------------------------------------
    # ['mil_forces', 'mil_forces_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'military_forces':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military and security forces",
            parser_function=parse_military_forces,
            iso3Code=iso3Code,
            parser_name="parse_military_forces"
        )
    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'Military and security service personnel strengths'
    # --------------------------------------------------------------------------------------------------
    military_personnel_strengths_data = mil_data.get(
        "Military and security service personnel strengths", {})
    # --------------------------------------------------------------------------------------------------
    # ['mil_person', 'mil_person_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'military_personnel':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military and security service personnel strengths",
            parser_function=parse_military_personnel,
            iso3Code=iso3Code,
            parser_name="parse_military_personnel"
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'Military deployments'
    # --------------------------------------------------------------------------------------------------
    military_deployments_data = mil_data.get("Military deployments", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'deployments':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military deployments",
            parser_function=parse_deployments,
            iso3Code=iso3Code,
            parser_name="parse_deployments"
        )

    # 5
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'Military equipment inventories and acquisitions'
    # --------------------------------------------------------------------------------------------------
    military_equipment_inventories_data = mil_data.get(
        "Military equipment inventories and acquisitions", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'military_inventories':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military equipment inventories and acquisitions",
            parser_function=parse_military_inventories,
            iso3Code=iso3Code,
            parser_name="parse_military_inventories"
        )

    # 6
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'Military expenditures'
    # --------------------------------------------------------------------------------------------------
    military_expenditures_data = mil_data.get("Military expenditures", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'military_expenditures':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military expenditures",
            parser_function=parse_military_expenditures,
            iso3Code=iso3Code,
            parser_name="parse_military_expenditures"
        )

    # 7
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7 >>> 'Military service age and obligation'
    # --------------------------------------------------------------------------------------------------
    military_service_age_obligation_data = mil_data.get(
        "Military service age and obligation", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'military_age':
        return extract_and_parse(
            main_data=mil_data,
            key_path="Military service age and obligation",
            parser_function=parse_military_age,
            iso3Code=iso3Code,
            parser_name="parse_military_age"
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':

    import platform
    # ---------------------------------------------------------------------------------------------------------------------------------
    info = 'military_expenditures'
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
        get_military(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
