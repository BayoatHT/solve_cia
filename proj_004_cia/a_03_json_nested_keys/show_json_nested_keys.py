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
from collections import defaultdict
from impact_titan.impact_3_data._config._DATA_CONFIG import DataConfig
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def show_json_nested_keys():

    # ESTABLISH FOLDER FOR THE CIA JSONS
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    # This is where we have saved the jsons for each country - separate json file(per region - folder)
    # --------------------------------------------------------------------------------------------------
    raw_data_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # Dictionary to store the generalized map of keys
    key_map = defaultdict(set)
    # //////////////////////////////////////////////////////////////////////////////////////////////////

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
        # --------------------------------------------------------------------------------------------------
        if cia_region in non_country_regions:
            continue
        else:
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
                # --------------------------------------------------------------------------------------------------
                file_path = os.path.join(cia_region_folder, file)
                with open(file_path, 'r', encoding='utf-8') as country_file:
                    data = json.load(country_file)

                # Update the generalized key map with this file's structure
                update_key_map(data, key_map)
                # --------------------------------------------------------------------------------------------------

    # Convert defaultdict of sets to a regular dictionary of lists for JSON serialization
    key_map_dict = {k: sorted(list(v)) for k, v in key_map.items()}
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WRITE FILE - use json to write the file
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    utils_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\a_03_json_nested_keys\utils'
    cia_file_name = 'cia_json_dict_map'
    cia_file = f'{cia_file_name}.py'
    cia_file_path = os.path.join(utils_folder, cia_file)
    # --------------------------------------------------------------------------------------------------
    with open(cia_file_path, 'w', encoding='utf-8') as cia_file:
        cia_file.write(
            f'{cia_file_name} = {json.dumps(key_map_dict, indent=4)}\n')

    # CONFIRMATION
    # ///////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    print(f'#/////////////////////////////////////////////////////////////////////////////////////////////////////////\n')
    print(f'Created a Dict Map for all jsons\n')
    print(f'#/////////////////////////////////////////////////////////////////////////////////////////////////////////\n')
    # //////////////////////////////////////////////////////////////////////////////////////////////////


def update_key_map(data, key_map, parent_key=''):
    """
    Recursively updates the generalized map of keys by adding any new keys found in the given data (which is expected to be a dictionary).
    """
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f'{parent_key}.{key}' if parent_key else key
            key_map[parent_key].add(key)
            if isinstance(value, dict):
                update_key_map(value, key_map, full_key)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    update_key_map(item, key_map, f'{full_key}[{index}]')
    elif isinstance(data, list):
        for index, item in enumerate(data):
            update_key_map(item, key_map, f'{parent_key}[{index}]')


def print_key_map(key_map):
    """
    Prints the generalized map of keys in a readable format.
    """
    for parent_key, sub_keys in key_map.items():
        if parent_key:
            print(f'{parent_key}: {sorted(sub_keys)}')
        else:
            print(f'Top-level keys: {sorted(sub_keys)}')


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':

    show_json_nested_keys()
