######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------

import os
import re
import json
import logging

# ---------------------------------------------------------------------------------------------------------------------
# Import helper functions from the __worker_utils directory
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.extract_numeric_value import extract_numeric_value
from proj_004_cia.c_00_transform_utils.parse_percentage_data import parse_percentage_data
from proj_004_cia.c_00_transform_utils.parse_list_from_string import parse_list_from_string
from proj_004_cia.c_00_transform_utils.parse_text_field import parse_text_field
from proj_004_cia.c_00_transform_utils.parse_text_and_note import parse_text_and_note
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.c_00_transform_utils.extract_and_parse import extract_and_parse
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.c_02_geography.helper.utils.parse_location import parse_location
from proj_004_cia.c_02_geography.helper.utils.parse_area_comparative import parse_area_comparative
from proj_004_cia.c_02_geography.helper.utils.parse_area_data import parse_area_data
from proj_004_cia.c_02_geography.helper.utils.parse_coastline_data import parse_coastline_data
from proj_004_cia.c_02_geography.helper.utils.parse_geographic_coordinates import parse_geographic_coordinates
from proj_004_cia.c_02_geography.helper.utils.parse_land_boundaries_master import parse_land_boundaries_master
from proj_004_cia.c_02_geography.helper.utils.parse_map_references import parse_map_references
from proj_004_cia.c_02_geography.helper.utils.parse_maritime_claims import parse_maritime_claims, parse_wld_maritime_claims
from proj_004_cia.c_02_geography.helper.utils.parse_terrain import parse_terrain
from proj_004_cia.c_02_geography.helper.utils.parse_wld_climate import parse_wld_climate
from proj_004_cia.c_02_geography.helper.utils.parse_wld_terrain import parse_wld_terrain
from proj_004_cia.c_02_geography.helper.utils.parse_elevation import parse_elevation, parse_wld_elevation
from proj_004_cia.c_02_geography.helper.utils.parse_land_use import parse_land_use
from proj_004_cia.c_02_geography.helper.utils.parse_irrigated_land import parse_irrigated_land
from proj_004_cia.c_02_geography.helper.utils.parse_major_lakes import parse_major_lakes, parse_wld_major_lakes
from proj_004_cia.c_02_geography.helper.utils.parse_major_rivers import parse_major_rivers, parse_wld_major_rivers
from proj_004_cia.c_02_geography.helper.utils.parse_major_watersheds import parse_major_watersheds
from proj_004_cia.c_02_geography.helper.utils.parse_major_aquifers import parse_major_aquifers, parse_wld_major_aquifers
from proj_004_cia.c_02_geography.helper.utils.parse_natural_resources import parse_natural_resources
from proj_004_cia.c_02_geography.helper.utils.parse_wonders_of_the_world import parse_wonders_of_the_world
from proj_004_cia.c_02_geography.helper.utils.parse_natural_hazards import parse_natural_hazards
from proj_004_cia.c_02_geography.helper.utils.parse_population_distribution import parse_population_distribution
from proj_004_cia.c_02_geography.helper.utils.parse_geography_note import parse_geography_note
from proj_004_cia.c_02_geography.helper.utils.parse_geography_world import parse_geography_world
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


# Configure logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------------------------------------------------------------------------------------------------------


def get_geography(data={}, info={}, iso3Code={}):
    """
    Function to extract geography information based on the 'info' parameter.
    """
    # Define 'geography' at the beginning of the function
    geography = data.get("Geography", {})

    if not geography:
        logging.warning(f"No 'Geography' section found for {iso3Code}")
        return {}

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # WORLD-SPECIFIC: Return comprehensive World geography data
    # --------------------------------------------------------------------------------------------------
    if info == 'world_geography' and iso3Code == 'WLD':
        return parse_geography_world(geography, iso3Code)

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'GEO AREA'
    # --------------------------------------------------------------------------------------------------
    if info == 'location':
        return extract_and_parse(
            main_data=geography,
            key_path="Location",
            parser_function=parse_location,
            iso3Code=iso3Code,
            parser_name="parse_location"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'GEOGRAPHIC OVERVIEW' (World data only)
    # --------------------------------------------------------------------------------------------------
    elif info == 'geographic_overview':
        # Check if iso3Code corresponds to 'World'
        if iso3Code != 'WLD':
            logging.warning(
                f"'Geographic overview' is only available for the World data.")
            return {}

        # Try to get the 'Geographic overview' data from 'Geography' section
        geographic_overview_data = data.get(
            "Geography", {}).get('Geographic overview', {})
        if not geographic_overview_data:
            logging.warning(
                f"No 'Geographic overview' data found for {iso3Code}")
            return {}

        text = geographic_overview_data.get('text', '')
        if not text:
            logging.warning(
                f"No text in 'Geographic overview' data for {iso3Code}")
            return {}

        # Clean the text (remove HTML tags and extra whitespace)
        cleaned_text = clean_text(text)

        return cleaned_text
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'GEOGRAPHIC COORDINATES'
    # --------------------------------------------------------------------------------------------------
    elif info == 'geographic_coordinates':
        return extract_and_parse(
            main_data=geography,
            key_path="Geographic coordinates",
            parser_function=parse_geographic_coordinates,
            iso3Code=iso3Code,
            parser_name="Geographic coordinates"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'MAP REFERENCES'
    # --------------------------------------------------------------------------------------------------
    elif info == 'map_references':
        return extract_and_parse(
            main_data=geography,
            key_path="Map references",
            parser_function=parse_map_references,
            iso3Code=iso3Code,
            parser_name="Map references"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'AREA'
    # --------------------------------------------------------------------------------------------------
    elif info == 'area_total':
        return extract_and_parse(
            main_data=geography,
            key_path="Area.total",
            parser_function=parse_area_data,
            iso3Code=iso3Code,
            parser_name="total area"
        )

    elif info == 'area_land':
        return extract_and_parse(
            main_data=geography,
            key_path="Area.land",
            parser_function=parse_area_data,
            iso3Code=iso3Code,
            parser_name="land area"
        )

    elif info == 'area_water':
        return extract_and_parse(
            main_data=geography,
            key_path="Area.water",
            parser_function=parse_area_data,
            iso3Code=iso3Code,
            parser_name="water area"
        )

    elif info == 'area_note':
        return extract_and_parse(
            main_data=geography,
            key_path="Area.note",
            parser_function=lambda data, _: re.sub(r'<[^>]+>', '', data),
            iso3Code=iso3Code,
            parser_name="area note"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'AREA - COMPARATIVE'
    # --------------------------------------------------------------------------------------------------
    elif info == 'area_comparative':
        return extract_and_parse(
            main_data=geography,
            key_path="Area - comparative",
            parser_function=parse_area_comparative,
            iso3Code=iso3Code,
            parser_name="Area - comparative"
        )
    # ----------------------------------------------------------------------------------------------------

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7A >>> 'LAND BOUNDARIES'
    # --------------------------------------------------------------------------------------------------
    elif info == 'land_boundaries':
        return extract_and_parse(
            main_data=geography,
            key_path="Land boundaries",
            parser_function=parse_land_boundaries_master,
            iso3Code=iso3Code,
            parser_name="Land boundaries"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7B >>> 'WLD LAND BOUNDARIES' (World data only)
    # --------------------------------------------------------------------------------------------------
    elif info == 'wld_land_boundaries':
        try:
            # Check if iso3Code corresponds to 'World'
            if iso3Code != 'WLD':
                logging.warning(
                    f"'World Land Boundaries' is only available for the World data.")
                return {}

            # Try to get the 'Land boundaries' data from 'Geography' section
            land_boundaries_data = geography.get('Land boundaries', {})
            if not land_boundaries_data:
                logging.warning(
                    f"No 'Land boundaries' data found for {iso3Code}")
                return {}

            # Attempt to retrieve 'text' within 'Land boundaries' data
            try:
                text = land_boundaries_data.get('text', '')
                if not text:
                    logging.warning(
                        f"No text in 'Land boundaries' data for {iso3Code}")
                    return {}

                # Clean the text (remove HTML tags and extra whitespace)
                cleaned_text = clean_text(text)
                return cleaned_text
            except Exception as e:
                logging.error(
                    f"Error accessing 'text' field in 'Land boundaries' data for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Land boundaries' data for {iso3Code}: {e}")
        return {}

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 8 >>> 'COASTLINE'
    # --------------------------------------------------------------------------------------------------
    elif info == 'coastline':
        return extract_and_parse(
            main_data=geography,
            key_path="Coastline",
            parser_function=parse_coastline_data,
            iso3Code=iso3Code,
            parser_name="Coastline"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 9 >>> 'MARITIME CLAIMS'
    # --------------------------------------------------------------------------------------------------
    elif info == 'maritime_claims':

        return extract_and_parse(
            main_data=geography,
            key_path="Maritime claims",
            parser_function=parse_maritime_claims,
            iso3Code=iso3Code,
            parser_name="Maritime claims"
        )

    elif info == 'wld_maritime_claims':
        try:
            # Try to extract 'Maritime claims' data
            maritime_claims_data = geography.get('Maritime claims', {})
            if not maritime_claims_data:
                logging.warning(
                    f"No 'Maritime claims' data found for world level processing")
                return {}

            # Try to parse the extracted data
            try:
                return parse_wld_maritime_claims(maritime_claims_data=maritime_claims_data)
            except Exception as e:
                logging.error(
                    f"Error in 'parse_wld_maritime_claims': {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Maritime claims' data for world level processing: {e}")
            return {}

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 10 >>> 'CLIMATE'
    # --------------------------------------------------------------------------------------------------
    elif info == 'climate':
        try:
            # Try to extract 'Climate' data
            climate_data = geography.get('Climate', {})
            if not climate_data:
                logging.warning(
                    f"No 'Climate' data found for {iso3Code}")
                return {}

            # Try to parse the extracted data
            try:
                return parse_text_and_note(data=climate_data, main_key='climate', iso3Code=iso3Code)
            except Exception as e:
                logging.error(
                    f"Error in 'parse_text_and_note' for 'climate' data for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Climate' data for {iso3Code}: {e}")
            return {}

    elif info == 'wld_climate':
        return extract_and_parse(
            main_data=geography,
            key_path="Climate",
            parser_function=parse_wld_climate,
            iso3Code=iso3Code,
            parser_name="World Climate",
            is_world_data=True
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 11 >>> 'TERRAIN'
    # --------------------------------------------------------------------------------------------------
    elif info == 'terrain':
        return extract_and_parse(
            main_data=geography,
            key_path="Terrain",
            parser_function=parse_terrain,
            iso3Code=iso3Code,
            parser_name="Terrain"
        )

    elif info == 'wld_terrain':
        return extract_and_parse(
            main_data=geography,
            key_path="Terrain",
            parser_function=parse_wld_terrain,
            iso3Code=iso3Code,
            parser_name="World Terrain",
            is_world_data=True
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 12 >>> 'ELEVATION'
    # --------------------------------------------------------------------------------------------------
    elif info == 'elevation':
        return extract_and_parse(
            main_data=geography,
            key_path="Elevation",
            parser_function=parse_elevation,
            iso3Code=iso3Code,
            parser_name="Elevation"
        )

    elif info == 'wld_elevation':
        return extract_and_parse(
            main_data=geography,
            key_path="Elevation",
            parser_function=parse_wld_elevation,
            iso3Code=iso3Code,
            parser_name="World Elevation",
            is_world_data=True
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'LAND USE'
    # --------------------------------------------------------------------------------------------------
    elif info == 'land_use':
        return extract_and_parse(
            main_data=geography,
            key_path="Land use",
            parser_function=parse_land_use,
            iso3Code=iso3Code,
            parser_name="Land use"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'IRRIGATED LAND'
    # --------------------------------------------------------------------------------------------------
    elif info == 'irrigated_land':
        return extract_and_parse(
            main_data=geography,
            key_path="Irrigated land",
            parser_function=parse_irrigated_land,
            iso3Code=iso3Code,
            parser_name="Irrigated land"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'MAJOR LAKES'
    # --------------------------------------------------------------------------------------------------
    elif info == 'major_lakes':
        return extract_and_parse(
            main_data=geography,
            key_path="Major lakes (area sq km)",
            parser_function=parse_major_lakes,
            iso3Code=iso3Code,
            parser_name="Major lakes"
        )

    elif info == 'wld_major_lakes':
        try:
            # Try to extract 'Major lakes (area sq km)' data
            wld_major_lakes = geography.get('Major lakes (area sq km)', {})
            if not wld_major_lakes:
                logging.warning(
                    f"No 'Major lakes (area sq km)' data found for {iso3Code}")
                return {}

            # Try to parse the extracted data
            try:
                return parse_wld_major_lakes(major_lakes_data=wld_major_lakes)
            except Exception as e:
                logging.error(
                    f"Error in 'parse_wld_major_lakes' for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Major lakes (area sq km)' data for {iso3Code}: {e}")
            return {}

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 14 >>> 'MAJOR RIVERS'
    # --------------------------------------------------------------------------------------------------
    elif info == 'major_rivers':
        return extract_and_parse(
            main_data=geography,
            key_path="Major rivers (by length in km)",
            parser_function=parse_major_rivers,
            iso3Code=iso3Code,
            parser_name="Major rivers (by length in km)"
        )

    elif info == 'wld_major_rivers':
        try:
            # Try to extract 'Major rivers (by length in km)' data
            wld_major_rivers = geography.get(
                'Major rivers (by length in km)', {})
            if not wld_major_rivers:
                logging.warning(
                    f"No 'Major rivers (by length in km)' data found for {iso3Code}")
                return {}

            # Try to parse the extracted data
            try:
                return parse_wld_major_rivers(major_rivers_data=wld_major_rivers)
            except Exception as e:
                logging.error(
                    f"Error in 'parse_wld_major_rivers' for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Major rivers (by length in km)' data for {iso3Code}: {e}")
            return {}
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 15 >>> 'MAJOR WATERSHEDS'
    # --------------------------------------------------------------------------------------------------
    elif info == 'major_watersheds':
        return extract_and_parse(
            main_data=geography,
            key_path="'Major watersheds (area sq km)",
            parser_function=parse_major_watersheds,
            iso3Code=iso3Code,
            parser_name="'Major watersheds (area sq km)"
        )

    elif info == 'wld_major_watersheds':
        try:
            # Try to get the 'Major watersheds (area sq km)' data from 'Geography' section
            wld_watershed_data = data.get("Geography", {}).get(
                'Major watersheds (area sq km)', {})
            if not wld_watershed_data:
                logging.warning(
                    f"No 'Major watersheds (area sq km)' data found for {iso3Code}")
                return {}

            text = wld_watershed_data.get('text', '')
            if not text:
                logging.warning(
                    f"No text in 'Major watersheds (area sq km)' data for {iso3Code}")
                return {}

            # Clean the text (remove HTML tags and extra whitespace)
            try:
                cleaned_text = clean_text(text)
                return cleaned_text
            except Exception as e:
                logging.error(
                    f"Error cleaning 'Major watersheds (area sq km)' text for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Major watersheds (area sq km)' data for {iso3Code}: {e}")
            return {}
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 16 >>> 'NATURAL RESOURCES'
    # --------------------------------------------------------------------------------------------------
    elif info == 'natural_resources':
        return extract_and_parse(
            main_data=geography,
            key_path="Natural resources",
            parser_function=parse_natural_resources,
            iso3Code=iso3Code,
            parser_name="Natural resources"
        )
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 16 >>> 'WONDERS OF THE WORLD'
    # --------------------------------------------------------------------------------------------------
    elif info == 'wonders_of_the_world':
        try:
            # Try to extract 'Wonders of the World' data
            wonders_data = geography.get('Wonders of the World', {})
            if not wonders_data:
                logging.warning(
                    f"No 'Wonders of the World' data found for {iso3Code}")
                return {}

            # Try to parse the extracted data
            try:
                return parse_wonders_of_the_world(wonders_data=wonders_data)
            except Exception as e:
                logging.error(
                    f"Error in 'parse_wonders_of_the_world' for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Wonders of the World' data for {iso3Code}: {e}")
            return {}

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 17 >>> 'NATURAL HAZARDS'
    # --------------------------------------------------------------------------------------------------
    elif info == 'natural_hazards':
        return extract_and_parse(
            main_data=geography,
            key_path="Natural hazards",
            parser_function=parse_natural_hazards,
            iso3Code=iso3Code,
            parser_name="Natural hazards"
        )
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 18 >>> 'MAJOR AQUIFERS'
    # --------------------------------------------------------------------------------------------------
    elif info == 'major_aquifers':
        return extract_and_parse(
            main_data=geography,
            key_path="Major aquifers",
            parser_function=parse_major_aquifers,
            iso3Code=iso3Code,
            parser_name="Major aquifers"
        )

    elif info == 'wld_major_aquifers':
        try:
            # Try to extract 'Major aquifers' data
            wld_major_aquifers_data = geography.get('Major aquifers', {})
            if not wld_major_aquifers_data:
                logging.warning(
                    f"No 'Major aquifers' data found for {iso3Code}")
                return {}

            # Try to parse the extracted data
            try:
                return parse_wld_major_aquifers(aquifers_data=wld_major_aquifers_data)
            except Exception as e:
                logging.error(
                    f"Error in 'parse_wld_major_aquifers' for {iso3Code}: {e}")
                return {}

        except Exception as e:
            logging.error(
                f"Error extracting 'Major aquifers' data for {iso3Code}: {e}")
            return {}

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 19 >>> 'POPULATION DISTRIBUTION'
    # --------------------------------------------------------------------------------------------------
    elif info == 'population_distribution':
        return extract_and_parse(
            main_data=geography,
            key_path="Population distribution",
            parser_function=parse_population_distribution,
            iso3Code=iso3Code,
            parser_name="Population distribution"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 20 >>> 'GEOGRAPHY NOTE'
    # --------------------------------------------------------------------------------------------------
    elif info == 'geography_note':
        return extract_and_parse(
            main_data=geography,
            key_path="Geography - note",
            parser_function=parse_geography_note,
            iso3Code=iso3Code,
            parser_name="Geography - noted"
        )

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # If 'info' doesn't match 'location', return {} or handle other cases
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    else:
        logging.warning(
            f"Info type '{info}' not implemented yet for {iso3Code}")
        return {}
# //////////////////////////////////////////////////////////////////////////////////////////////////////


# --------------------------------------------------------------------------------------------
######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    # --------------------------------------------------------------------------------------------------
    info = 'maritime_claims'
    # ---------------------------
    country = "USA"
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
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
        get_geography(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
