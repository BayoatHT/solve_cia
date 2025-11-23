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
# get_transportation ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_09_transportation.helper.get_transportation import get_transportation


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_transportation_data(
    data: dict,
    iso3Code: str
):

    # 9. TRANSPORTATION
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # WORLD-SPECIFIC: Use comprehensive World parser
    if iso3Code == 'WLD':
        cia_pack['world_transportation'] = get_transportation(
            data=data, info='world_transportation', iso3Code=iso3Code)
        return cia_pack

    # Conditional inclusion for individual countries
    if iso3Code != 'WLD':
        # Note: 'airports'
        cia_pack['airports'] = get_transportation(
            data=data, info='airports', iso3Code=iso3Code)
        # Note: 'airports_paved'
        cia_pack['airports_paved'] = get_transportation(
            data=data, info='airports_paved', iso3Code=iso3Code)
        # Note: 'airports_unpaved'
        cia_pack['airports_unpaved'] = get_transportation(
            data=data, info='airports_unpaved', iso3Code=iso3Code)
        # Note: 'civil_reg_code'
        cia_pack['civil_reg_code'] = get_transportation(
            data=data, info='civil_reg_code', iso3Code=iso3Code)
        # Note: 'heliports'
        cia_pack['heliports'] = get_transportation(
            data=data, info='heliports', iso3Code=iso3Code)
        # Note: 'merchant_marine'
        cia_pack['merchant_marine'] = get_transportation(
            data=data, info='merchant_marine', iso3Code=iso3Code)
        # Note: 'air_system'
        cia_pack['air_system'] = get_transportation(
            data=data, info='air_system', iso3Code=iso3Code)
        # Note: 'pipelines'
        cia_pack['pipelines'] = get_transportation(
            data=data, info='pipelines', iso3Code=iso3Code)
        # Note: 'ports'
        cia_pack['ports'] = get_transportation(
            data=data, info='ports', iso3Code=iso3Code)
        # Note: 'ports_and_terminals'
        cia_pack['ports_and_terminals'] = get_transportation(
            data=data, info='ports_and_terminals', iso3Code=iso3Code)
        # Note: 'railways'
        cia_pack['railways'] = get_transportation(
            data=data, info='railways', iso3Code=iso3Code)
        # Note: 'roadways'
        cia_pack['roadways'] = get_transportation(
            data=data, info='roadways', iso3Code=iso3Code)
        # Note: 'transportation_note'
        cia_pack['transportation_note'] = get_transportation(
            data=data, info='transportation_note', iso3Code=iso3Code)
        # Note: 'waterways'
        cia_pack['waterways'] = get_transportation(
            data=data, info='waterways', iso3Code=iso3Code)
    else:
        # Note: ''
        pass

    # Return the compiled geography data
    return cia_pack


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
    pprint(return_transportation_data(data=data, iso3Code=iso3Code))
