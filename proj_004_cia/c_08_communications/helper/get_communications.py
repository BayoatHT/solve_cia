######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import json
import logging
# --------------------------------------------------------------------------------------------------
# NOTE: "Broadband - fixed subscriptions"
# >>> ['broadband_note', 'broadband_subs_per_100', 'broadband_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_broadband_fixed import parse_broadband_fixed
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Broadcast media"
# >>> ['broadcast_media]
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_broadband_media import parse_broadband_media
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Communications - note"
# >>> ['communications_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_communications_note import parse_communications_note
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Internet country code"
# >>> ['internet_country_code', 'internet_country_code_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_internet_code import parse_internet_code
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Internet users"
# >>> ['internet_users_note', 'internet_users_percent', 'internet_users_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_internet_users import parse_internet_users
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Telecommunication systems"
# >>> ['telecom_domestic', 'telecom_general_assessment', 'telecom_international', 'telecom_note', 'telecom_overseas_departments']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_tele_systems import parse_tele_systems
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Telephones - fixed lines"
# >>> ['fixed_phone_note', 'fixed_phone_subs_per_100', 'fixed_phone_total_subs']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_phone_fixed_lines import parse_phone_fixed_lines
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Telephones - mobile cellular"
# >>> ['mobile_phone_note', 'mobile_phone_subs_per_100', 'mobile_phone_total_subs']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_08_communications.helper.utils.parse_phone_mobile_cellular import parse_phone_mobile_cellular
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -------------------------------------------------------------------------------------------------
# #////////////////////////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////////////////////////////////////////


from proj_004_cia.c_08_communications.helper.utils.parse_communications_world import parse_communications_world


def get_communications(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: COMMUNICATIONS DATA
    # --------------------------------------------------------------------------------------------------
    comms_data = data.get("Communications", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WORLD-SPECIFIC: Return comprehensive World communications data
    if info == 'world_communications' and iso3Code == 'WLD':
        return parse_communications_world(comms_data, iso3Code)

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'Broadband - fixed subscriptions'
    # --------------------------------------------------------------------------------------------------
    broadband_fixed_subscriptions_data = comms_data.get(
        "Broadband - fixed subscriptions", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'broadband_fixed':
        return parse_broadband_fixed(
            broadband_fixed_subscriptions_data
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'Broadcast media'
    # --------------------------------------------------------------------------------------------------
    broadcast_media_data = comms_data.get("Broadcast media", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'broadband_media':
        return parse_broadband_media(
            broadcast_media_data
        )

    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'Communications - note'
    # --------------------------------------------------------------------------------------------------
    communications_note_data = comms_data.get("Communications - note", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'communications_note':
        return parse_communications_note(
            communications_note_data
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'Internet country code'
    # --------------------------------------------------------------------------------------------------
    internet_country_code_data = comms_data.get("Internet country code", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'internet_code':
        return parse_internet_code(
            internet_country_code_data
        )

    # 5
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'Internet users'
    # --------------------------------------------------------------------------------------------------
    internet_users_data = comms_data.get("Internet users", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'internet_users_note'
    # "percent of population" - 'internet_users_percent'
    # "total" - 'internet_users_total'
    # --------------------------------------------------------------------------------------------------
    # ['internet_users_note', 'internet_users_percent', 'internet_users_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'internet_users':
        return parse_internet_users(
            internet_users_data
        )

    # 6
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'Telecommunication systems'
    # --------------------------------------------------------------------------------------------------
    telecommunication_systems_data = comms_data.get(
        "Telecommunication systems", {})
    # --------------------------------------------------------------------------------------------------
    # "domestic" - 'telecom_domestic'
    # "general assessment" - 'telecom_general_assessment'
    # "international" - 'telecom_international'
    # "note" - 'telecom_note'
    # "overseas departments" - 'telecom_overseas_departments'
    # --------------------------------------------------------------------------------------------------
    # ['telecom_domestic', 'telecom_general_assessment', 'telecom_international', 'telecom_note', 'telecom_overseas_departments']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'tele_systems':
        return parse_tele_systems(
            telecommunication_systems_data
        )

    # 7
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7 >>> 'Telephones - fixed lines'
    # --------------------------------------------------------------------------------------------------
    telephones_fixed_lines_data = comms_data.get(
        "Telephones - fixed lines", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'fixed_phone_note'
    # "subscriptions per 100 inhabitants" - 'fixed_phone_subs_per_100'
    # "total subscriptions" - 'fixed_phone_total_subs'
    # --------------------------------------------------------------------------------------------------
    # ['fixed_phone_note', 'fixed_phone_subs_per_100', 'fixed_phone_total_subs']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'phone_fixed_lines':
        return parse_phone_fixed_lines(
            telephones_fixed_lines_data
        )

    # 8
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 8 >>> 'Telephones - mobile cellular'
    # --------------------------------------------------------------------------------------------------
    telephones_mobile_cellular_data = comms_data.get(
        "Telephones - mobile cellular", {})
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'phone_mobile_cellular':
        return parse_phone_mobile_cellular(
            telephones_mobile_cellular_data
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    import platform
    # ---------------------------------------------------------------------------------------------------------------------------------
    info = 'pass'
    # ---------------------------------------------------------------------------------------------------------------------------------
    country = "USA"
    # ----------------------------------------------------------------------------------------------------------------------------------
    if platform.system() == 'Windows':
        json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    else:
        json_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '_raw_data')
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
        get_communications(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
