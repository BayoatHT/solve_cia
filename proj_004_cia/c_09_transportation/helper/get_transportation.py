######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import json
import logging
# --------------------------------------------------------------------------------------------------
# NOTE: "Airports" - ['airports', 'airports_note']
# >>> ['airports', 'airports_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_airports import parse_airports
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Airports - with paved runways"
# >>> ['paved_runways_total', 'paved_runways_1_2']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_airports_paved import parse_airports_paved
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Airports - with unpaved runways"
# >>>  ['unpaved_runways_total', 'unpaved_runways_0_1', 'unpaved_runways_1_2', 'unpaved_runways_under_914_m']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_airports_unpaved import parse_airports_unpaved
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Civil aircraft registration country code prefix"
# >>> ['civil_reg_code']
from proj_004_cia.c_09_transportation.helper.utils.parse_civil_reg_code import parse_civil_reg_code
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Heliports"
# >>> ['heliports']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_heliports import parse_heliports
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Merchant marine"
# >>> ['merchant_marine_total', 'merchant_marine_by_type', 'merchant_marine_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_merchant_marine import parse_merchant_marine
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "National air transport system"
# >>> [ 'annual_freight', 'annual_passenger', 'inventory_aircraft', 'num_reg_aircraft']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_air_system import parse_air_system
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Pipelines"
# >>> ["pipelines"]
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_pipelines import parse_pipelines
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Ports"
# >>> ['key_ports', 'large_ports', 'medium_ports', 'ports_with_oil_terminals',
# 'ports_size_unknown', 'small_ports', 'total_ports', 'very_small_ports']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_ports import parse_ports
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Ports and terminals"
# >>> ['major_seaports']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_ports_and_terminals import parse_ports_and_terminals
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Railways"
# >>> ['railways_broad', 'railways_dual', 'railways_narrow', 'railways_note', 'railways_standard', 'railways_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_railways import parse_railways
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Roadways"
# >>> ['turkish_roadways', 'non_urban_roadways', 'roadways_note', 'paved_roadways',
# 'private_forest_roadways', 'total_roadways', 'unpaved_roadways', 'urban_roadways']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_roadways import parse_roadways
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Transportation - note"
# >>> ['transportation_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_transportation_note import parse_transportation_note
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Waterways"
# >>> ['waterways', 'waterways_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.utils.parse_waterways import parse_waterways
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -------------------------------------------------------------------------------------------------
# #////////////////////////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////////////////////////////////////////


from proj_004_cia.c_09_transportation.helper.utils.parse_transportation_world import parse_transportation_world


def get_transportation(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: TRANSPORTATION DATA
    # --------------------------------------------------------------------------------------------------
    transport_data = data.get("Transportation", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WORLD-SPECIFIC: Return comprehensive World transportation data
    if info == 'world_transportation' and iso3Code == 'WLD':
        return parse_transportation_world(transport_data, iso3Code)

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'Airports'
    # --------------------------------------------------------------------------------------------------
    airports_data = transport_data.get("Airports", {})
    # --------------------------------------------------------------------------------------------------
    # ['airports', 'airports_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'airports':
        return parse_airports(
            airports_data, iso3Code
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'Airports - with paved runways'
    # --------------------------------------------------------------------------------------------------
    airports_paved_data = transport_data.get(
        "Airports - with paved runways", {})
    # --------------------------------------------------------------------------------------------------
    # ['paved_runways_total', 'paved_runways_1_2']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'airports_paved':
        return parse_airports_paved(
            airports_paved_data, iso3Code
        )

    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'Airports - with unpaved runways'
    # --------------------------------------------------------------------------------------------------
    airports_unpaved_data = transport_data.get(
        "Airports - with unpaved runways", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'airports_unpaved':
        return parse_airports_unpaved(
            airports_unpaved_data, iso3Code
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'Civil aircraft registration country code prefix'
    # --------------------------------------------------------------------------------------------------
    civil_aircraft_code_prefix_data = transport_data.get(
        "Civil aircraft registration country code prefix", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'civil_reg_code':
        return parse_civil_reg_code(
            civil_aircraft_code_prefix_data, iso3Code
        )

    # 5
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'Heliports'
    # --------------------------------------------------------------------------------------------------
    heliports_data = transport_data.get("Heliports", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'heliports':
        return parse_heliports(
            heliports_data, iso3Code
        )

    # 6
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'Merchant marine'
    # --------------------------------------------------------------------------------------------------
    merchant_marine_data = transport_data.get("Merchant marine", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'merchant_marine':
        return parse_merchant_marine(
            merchant_marine_data, iso3Code
        )

    #####################################################################################################
    #####################################################################################################

    # 7
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7 >>> 'National air transport system'
    # --------------------------------------------------------------------------------------------------
    national_air_transport_system_data = transport_data.get(
        "National air transport system", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'air_system':
        return parse_air_system(
            national_air_transport_system_data, iso3Code
        )

    # 8
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 8 >>> 'Pipelines'
    # --------------------------------------------------------------------------------------------------
    pipelines_data = transport_data.get("Pipelines", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'pipelines':
        return parse_pipelines(
            pipelines_data, iso3Code
        )

    # 9
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 9 >>> 'Ports'
    # --------------------------------------------------------------------------------------------------
    ports_data = transport_data.get("Ports", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'ports':
        return parse_ports(
            ports_data, iso3Code
        )

    # 10
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 10 >>> 'Ports and terminals'
    # --------------------------------------------------------------------------------------------------
    ports_terminals_data = transport_data.get("Ports and terminals", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'ports_and_terminals':
        return parse_ports_and_terminals(
            ports_terminals_data, iso3Code
        )

    # 11
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 11 >>> 'Railways'
    # --------------------------------------------------------------------------------------------------
    railways_data = transport_data.get("Railways", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'railways':
        return parse_railways(
            railways_data, iso3Code
        )

    # 12
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 12 >>> 'Roadways'
    # --------------------------------------------------------------------------------------------------
    roadways_data = transport_data.get("Roadways", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'roadways':
        return parse_roadways(
            roadways_data, iso3Code
        )

    # 13
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'Transportation - note'
    # --------------------------------------------------------------------------------------------------
    transportation_note_data = transport_data.get("Transportation - note", {})
    # --------------------------------------------------------------------------------------------------
    # ['transportation_note']
    if info == 'transportation_note':
        return parse_transportation_note(
            transportation_note_data, iso3Code
        )

    # 14
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 14 >>> 'Waterways'
    # --------------------------------------------------------------------------------------------------
    waterways_data = transport_data.get("Waterways", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'waterways':
        return parse_waterways(
            waterways_data, iso3Code
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':

    import platform
    # ---------------------------------------------------------------------------------------------------------------------------------
    info = 'airports'
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
        get_transportation(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
