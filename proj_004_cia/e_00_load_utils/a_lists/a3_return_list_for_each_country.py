'''
#   PURPOSE OF THIS FILE

NOTE:
    1. 
    2. 
    3. 
'''


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
from slugify import slugify
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.e_00_load_utils.a_lists.a1_list_paths import list_paths
from proj_004_cia.x_return.return_country_cia_data import return_country_cia_data
# ---------------------------------------------------------------------------------------------------------------------


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
def return_list_for_each_country(
    category_name=None,
):

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : GRACEFULLY HANDLE IF category_name not in list_paths
    # -----------------------------------------------------------------------------------------------------------------
    if category_name not in list_paths:
        return f"Error: {category_name} not in list_paths"

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : SOURCE - ACESS ORIGINAL FOLDER WHERE SOURCE IS KEPT
    # -----------------------------------------------------------------------------------------------------------------
    base_source = r"C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_data_per_country"

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : SOURCE - READ ALL FILE NAMES IN base_source - remove "_cia_meta.py" from the file name
    # -----------------------------------------------------------------------------------------------------------------
    all_files = [f for f in os.listdir(base_source) if f.endswith('.py')]
    all_iso_codes = [f.replace('_cia_meta.py', '') for f in all_files]
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : SOURCE - GET THE CATEGORY PATH
    # -----------------------------------------------------------------------------------------------------------------
    # eg.geography.natural_resources.natural_resources.main
    category_path = list_paths.get(category_name, '')

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : ESTABLISH DATA
    # ------------------------------------------------------------------------------------------------------------------
    each_list_data = {}

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : ITERATE OVER ALL ISO CODES
    # -----------------------------------------------------------------------------------------------------------------
    for iso_code in all_iso_codes:
        # Set category_path based on the condition for FRA and main_resources
        if iso_code == "FRA" and category_name == "main_resources":
            category_path = "geography.natural_resources.natural_resources.metropolitan_france"
        else:
            category_path = list_paths.get(category_name, '')

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # NOTE : COUNTRY DATA
        # -----------------------------------------------------------------------------------------------------------------
        country_data = return_country_cia_data(
            iso_code=iso_code
        )

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # NOTE : ACCESS THE DATA @ categoty_path
        # -----------------------------------------------------------------------------------------------------------------
        # Dynamically access nested dictionary data based on the category path
        if category_path:

            keys = category_path.split('.')
            try:
                # Traverse the dictionary using the keys in the category path
                data = country_data
                for key in keys:
                    data = data[key]  # Access nested dictionary level
            except KeyError:
                print(f"Error >> {iso_code} >> No Data >>'{category_path}'")
                # return []
            except TypeError:
                return "Error: Non-dictionary value encountered while accessing path"

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # NOTE : ADD THE DATA TO unique_items
        # -----------------------------------------------------------------------------------------------------------------
        import re
        if data is not None:
            key_version_of_items = []
            if isinstance(data, list):
                # Create an empty set to store unique items
                clean_unique_items_set = set()
                for item in data:
                    # Remove "and" only if it appears at the start
                    cleaned_item = re.sub(r'^(and|some)\s*', '', item) \
                        .replace("</P>", "") \
                        .replace("</p>", "") \
                        .replace("<P>", "") \
                        .replace("<p>", "") \
                        .strip()

                    # Split by semicolon if it exists, and add each part to the set
                    split_items = cleaned_item.split(';')
                    for part in split_items:
                        clean_unique_items_set.add(part.strip())

                # Convert the set back to a list
                all_unique_items = list(clean_unique_items_set)
                for clean_item in all_unique_items:
                    key_version_of_items.append(
                        slugify(clean_item, separator='_'))
                each_list_data[iso_code] = key_version_of_items

            else:
                print(
                    f"Error >> {iso_code} >> Not a list data type at '{category_path}': {type(data)}")

    return each_list_data


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    category_name = "main_resources"
    # -----------------------------------------------------------------------------------------------------------------
    print(
        return_list_for_each_country(
            category_name=category_name,
        ))
