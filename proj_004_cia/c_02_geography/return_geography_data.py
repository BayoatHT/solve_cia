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
# get_geography ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_02_geography.helper.get_geography import get_geography

######################################################################################################################
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def return_geography_data(
        data: dict,
        iso3Code: str
):
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # Conditional inclusion based on iso3Code
    if iso3Code == 'WLD':
        # WORLD-SPECIFIC: Use comprehensive World parser for consolidated rankings/statistics
        cia_pack['world_geography'] = get_geography(
            data=data, info='world_geography', iso3Code=iso3Code)
        # Include 'geographic_overview' for World data
        cia_pack['geographic_overview'] = get_geography(
            data=data, info='geographic_overview', iso3Code=iso3Code)
    else:
        # Include 'location' for other countries
        cia_pack['location'] = get_geography(
            data=data, info='location', iso3Code=iso3Code)
        # Include 'geographic_coordinates' for other countries
        cia_pack['geographic_coordinates'] = get_geography(
            data=data, info='geographic_coordinates', iso3Code=iso3Code)
        # Include 'map_references' for other countries
        cia_pack['map_references'] = get_geography(
            data=data, info='map_references', iso3Code=iso3Code)
    # Include 'population_distribution' for other countries
    cia_pack['population_distribution'] = get_geography(
        data=data, info='population_distribution', iso3Code=iso3Code)

    # Assign other entries directly
    # Note: 'geo_area'
    cia_pack['geo_area_total_sq_km'] = get_geography(
        data=data, info='area_total', iso3Code=iso3Code)
    cia_pack['geo_area_land_sq_km'] = get_geography(
        data=data, info='area_land', iso3Code=iso3Code)
    cia_pack['geo_area_water_sq_km'] = get_geography(
        data=data, info='area_water', iso3Code=iso3Code)
    cia_pack['geo_area_note'] = get_geography(
        data=data, info='area_note', iso3Code=iso3Code)

    # Note: 'geo_comparative'
    cia_pack['geo_area_comparative'] = get_geography(
        data=data, info='area_comparative', iso3Code=iso3Code)
    # Note: 'geo_coastline'
    cia_pack['coastline'] = get_geography(
        data=data, info='coastline', iso3Code=iso3Code)

    # Entries not applicable to World data
    if iso3Code != 'WLD':
        # Note: 'geo_land_boundaries'
        cia_pack['land_boundaries'] = get_geography(
            data=data, info='land_boundaries', iso3Code=iso3Code)
        # Note: 'maritime_claims'
        cia_pack['maritime_claims'] = get_geography(
            data=data, info='maritime_claims', iso3Code=iso3Code)
        # Note: 'climate'
        cia_pack['climate'] = get_geography(
            data=data, info='climate', iso3Code=iso3Code)
        # Note: 'terrain'
        cia_pack['terrain'] = get_geography(
            data=data, info='terrain', iso3Code=iso3Code)
        # Note: 'elevation'
        cia_pack['elevation'] = get_geography(
            data=data, info='elevation', iso3Code=iso3Code)
        # Note: 'land_use'
        cia_pack['land_use'] = get_geography(
            data=data, info='land_use', iso3Code=iso3Code)
        # Note: 'major_lakes'
        cia_pack['major_lakes'] = get_geography(
            data=data, info='major_lakes', iso3Code=iso3Code)
        # Note: 'major_rivers'
        cia_pack['major_rivers'] = get_geography(
            data=data, info='major_rivers', iso3Code=iso3Code)
        # Note: 'major_watersheds'
        cia_pack['major_watersheds'] = get_geography(
            data=data, info='major_watersheds', iso3Code=iso3Code)
        # Note: 'natural_resources'
        cia_pack['natural_resources'] = get_geography(
            data=data, info='natural_resources', iso3Code=iso3Code)
        # Note: 'major_aquifers'
        cia_pack['major_aquifers'] = get_geography(
            data=data, info='major_aquifers', iso3Code=iso3Code)
    else:
        cia_pack['wld_land_boundaries'] = get_geography(
            data=data, info='wld_land_boundaries', iso3Code=iso3Code)
        # Note: 'maritime_claims'
        cia_pack['wld_maritime_claims'] = get_geography(
            data=data, info='wld_maritime_claims', iso3Code=iso3Code)
        # Note: 'wld_climate'
        cia_pack['wld_climate'] = get_geography(
            data=data, info='wld_climate', iso3Code=iso3Code)
        # Note: 'terrain'
        cia_pack['wld_terrain'] = get_geography(
            data=data, info='wld_terrain', iso3Code=iso3Code)
        # Note: 'wld_elevation'
        cia_pack['wld_elevation'] = get_geography(
            data=data, info='wld_elevation', iso3Code=iso3Code)
        # Note: 'wld_major_lakes'
        cia_pack['wld_major_lakes'] = get_geography(
            data=data, info='wld_major_lakes', iso3Code=iso3Code)
        # Note: 'wld_major_rivers'
        cia_pack['wld_major_rivers'] = get_geography(
            data=data, info='wld_major_rivers', iso3Code=iso3Code)
        # Note: 'wld_major_watersheds'
        cia_pack['wld_major_watersheds'] = get_geography(
            data=data, info='wld_major_watersheds', iso3Code=iso3Code)
        # Note: 'wld_major_aquifers'
        cia_pack['wld_major_aquifers'] = get_geography(
            data=data, info='wld_major_aquifers', iso3Code=iso3Code)
        # Note: 'wonders_of_the_world'
        cia_pack['wonders_of_the_world'] = get_geography(
            data=data, info='wonders_of_the_world', iso3Code=iso3Code)

    # Note: 'irrigated_land'
    cia_pack['irrigated_land'] = get_geography(
        data=data, info='irrigated_land', iso3Code=iso3Code)
    # Note: 'natural_hazards'
    cia_pack['natural_hazards'] = get_geography(
        data=data, info='natural_hazards', iso3Code=iso3Code)
    # Note: 'geography_note'
    cia_pack['geography_note'] = get_geography(
        data=data, info='geography_note', iso3Code=iso3Code)

    # Return the compiled geography data
    return cia_pack


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
    pprint(return_geography_data(data=data, iso3Code=iso3Code))
