'''
#   PURPOSE OF THIS FILE

Instructions:
    1. 
    2. 
    3. 
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
# READ COUNTRY META DATA
###################################################################################################
from proj_004_cia.__utils.e_Original.base_country_meta import base_country_meta
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.a_01_cia_to_iso.utils.country_name_to_code import country_name_to_code
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.a_01_cia_to_iso.utils.cia_region_names import cia_region_names
# ---------------------------------------------------------------------------------------------------------------------
######################################################################################################################
#   CORE FUNCTION proj_004_cia\__utils\e_Original
# ---------------------------------------------------------------------------------------------------------------------


def create_cia_code_to_iso():

    # ESTABLISH FOLDER FOR THE CIA JSONS
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    # This is where we have saved the jsons for each country - separate json file(per region - folder)
    # C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia
    # --------------------------------------------------------------------------------------------------
    raw_data_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # GENERATE ISO 2 TO 3 CODES
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    # CREATE A LIST OUT OF EVERY KEY IN THE COUNTRIES META DATA
    ###################################################################################################
    countryCodes = list(base_country_meta.keys())
    # --------------------------------------------------------------------------------------------------
    # CREATE A DICTIONARY OF ISO2 AND ISO3 CODES
    ###################################################################################################
    iso3to2 = {
        'WLD': 'XX',
    }
    # ITERATE OVER THE COUNTRY CODES
    ###################################################################################################
    for countryCode in countryCodes:
        # GET THE ISO2 AND ISO3 CODES
        ###################################################################################################
        iso2Code = base_country_meta[countryCode]['iso2Code']
        iso3Code = base_country_meta[countryCode]['iso3Code']
        # ADD TO THE DICTIONARY
        ###################################################################################################
        iso3to2[iso3Code] = iso2Code

    missing_iso3 = []
    # PLACE HOLDER FOR THE CIA CODE NAME
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    cia_code_name = {
        'ee': {
            'cia_code': 'ee',
            'country_name': 'European Union',
            'region_name': 'europe',
            'iso2Code': '',
            'iso3Code': 'EEU'
        },
        'xx': {
            'cia_code': 'xx',
            'country_name': 'World',
            'region_name': 'world',
            'iso2Code': '',
            'iso3Code': 'WLD'
        },
    }

    # READ EACH FOLDER ¬ THEIR RESPECTIVE FILES IN THE JSONS FOLDER
    # ///////////////////////////////////////////////////////////////////////////////////////////////////

    # Establish non country region folders
    # --------------------------------------------------------------------------------------------------
    non_country_regions = ['antarctica', 'meta', 'oceans']

    # list all directories in the jsons folder
    # --------------------------------------------------------------------------------------------------
    all_directories = os.listdir(raw_data_folder)
    # --------------------------------------------------------------------------------------------------

    # iterate over the directories
    # --------------------------------------------------------------------------------------------------
    # for each file in subfolder, create a new key in the original_cia_meta dict
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    for cia_region in all_directories:
        if cia_region in non_country_regions:
            continue
        else:
            # --------------------------------------------------------------------------------------------------
            # get the region name
            region_name = cia_region_names[cia_region]
            # --------------------------------------------------------------------------------------------------
            # get the folder path
            cia_region_folder = os.path.join(raw_data_folder, cia_region)
            # --------------------------------------------------------------------------------------------------
            # get the files in the folder
            all_files = os.listdir(cia_region_folder)
            # --------------------------------------------------------------------------------------------------

            # //////////////////////////////////////////////////////////////////////////////////////////////////
            # iterate over the files - create a new key in the original_cia_meta dict
            # --------------------------------------------------------------------------------------------------
            for file in all_files:
                # remove the .json extension
                # --------------------------------------------------------------------------------------------------
                cia_file_code = file.replace('.json', '')
                # file iso3 code
                # --------------------------------------------------------------------------------------------------
                # get the file path
                file_path = os.path.join(cia_region_folder, file)
                try:
                    # open the file
                    with open(file_path, 'r', encoding='utf-8') as country_file:
                        # read the file
                        data = json.load(country_file)

                    # Try to access the nested key
                    try:
                        country_name = data['Government']['Country name']['conventional short form']['text']
                        # check if the country name is 'none'
                        # --------------------------------------------------------------------------------------------------
                        if country_name == 'none':
                            country_name = data['Government']['Country name']['conventional long form']['text']

                        # --------------------------------------------------------------------------------------------------
                        # check if we have a name to iso3Code relationship
                        # --------------------------------------------------------------------------------------------------
                        if country_name in country_name_to_code:
                            iso3Code = country_name_to_code[country_name]
                        else:
                            # check if a match will happen using bk county names
                            # --------------------------------------------------------------------------------------------------
                            bk_county_name = {
                                'Cabo Verde': 'Cape Verde',
                                'Congo (Brazzaville)': 'Republic of the Congo',
                                'DRC': 'Democratic Republic of the Congo',
                                'United States': 'United States of America',
                                "Cote d'Ivoire": "Ivory Coast",
                                'Sao Tome and Principe': 'São Tomé and Príncipe',
                                'Holy See (Vatican City)': 'Vatican City',
                                'Falkland Islands (Islas Malvinas)': 'Falkland Islands',
                                'South Georgia and South Sandwich Islands': 'South Georgia and the South Sandwich Islands',
                                'Czechia': 'Czech Republic',
                                'Timor-Leste': 'East Timor',
                                'Laos&nbsp;': 'Laos',
                                'The Dominican': 'Dominican Republic',
                                'Saint Barthelemy': 'Saint Barthélemy',
                                'Curacao': 'Curaçao',
                                'Virgin Islands': 'United States Virgin Islands',
                                'Burma': 'Myanmar',
                                'China': 'People\'s Republic of China',
                                'Saint Helena, Ascension, and Tristan da Cunha': 'Saint Helena',
                                'Baker Island, Howland Island, Jarvis Island, Johnston Atoll, Kingman Reef, Midway Islands, Palmyra Atoll': 'United States Minor Outlying Islands',
                            }
                            # --------------------------------------------------------------------------------------------------
                            if country_name in bk_county_name:
                                country_name = bk_county_name[country_name]
                                # check if we have a name to iso3Code relationship
                                # --------------------------------------------------------------------------------------------------
                                if country_name in country_name_to_code:
                                    iso3Code = country_name_to_code[country_name]
                                else:
                                    iso3Code = ''
                                    missing_iso3.append(country_name)
                            else:
                                iso3Code = ''
                                missing_iso3.append(country_name)
                        # --------------------------------------------------------------------------------------------------
                        # check if we have a corresponding iso2Code
                        # --------------------------------------------------------------------------------------------------
                        if iso3Code in iso3to2:
                            iso2Code = iso3to2[iso3Code]
                        else:
                            iso2Code = ''
                        # --------------------------------------------------------------------------------------------------
                        # Check if the country_name exists and is not empty
                        if country_name:
                            # add the cia code to the cia_code_name dict
                            cia_code_name[cia_file_code] = {
                                'country_name': country_name,
                                'region_name': region_name,
                                'iso3Code': iso3Code,
                                'iso2Code': iso2Code,
                                'cia_code': cia_file_code
                            }

                        else:
                            print(
                                f"Missing or empty country name for file {cia_file_code}")

                    except KeyError as e:
                        print(
                            f"KeyError: Missing key {e} in file {cia_file_code} >> {cia_region}")

                except Exception as e:
                    print(f"Failed to process file {cia_file_code}: {e}")
                # --------------------------------------------------------------------------------------------------

    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WRITE FILE - use json to write the file
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    utils_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\a_02_cia_area_codes\utils'
    cia_file_name = 'cia_code_names'
    cia_file = f'{cia_file_name}.py'
    cia_file_path = os.path.join(utils_folder, cia_file)
    # --------------------------------------------------------------------------------------------------
    with open(cia_file_path, 'w', encoding='utf-8') as cia_file:
        cia_file.write(
            f'{cia_file_name} = {json.dumps(cia_code_name, indent=4)}')

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # CONFIRMATION
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    print(f'#/////////////////////////////////////////////////////////////////////////////////////////////////////////\n')
    print(f'Original CIA Code names generated\n')
    print(f'#/////////////////////////////////////////////////////////////////////////////////////////////////////////\n')


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':

    create_cia_code_to_iso()
