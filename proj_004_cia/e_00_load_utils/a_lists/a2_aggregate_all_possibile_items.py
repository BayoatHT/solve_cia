import os
import re
import importlib
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.e_00_load_utils.a_lists.a1_list_paths import list_paths
from proj_004_cia.x_return.return_country_cia_data import return_country_cia_data
from proj_004_cia.a_02_cia_area_codes.iso3Code_to_cia_code import iso3Code_to_cia_code
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def aggregate_all_possible_items(
    category_name=None,
):
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: GRACEFULLY HANDLE IF category_name not in list_paths
    # -----------------------------------------------------------------------------------------------------------------
    if category_name not in list_paths:
        return f"Error: {category_name} not in list_paths"

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 2: ESTBALISH BASE FOLDER
    # -----------------------------------------------------------------------------------------------------------------
    base_folder_os = r"C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_data_per_country"

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 3: READ ALL FILE NAMES IN base_folder_os - remove "_cia_meta.py" from the file name
    # -----------------------------------------------------------------------------------------------------------------
    all_files = [f for f in os.listdir(base_folder_os) if f.endswith('.py')]
    all_iso_codes = [f.replace('_cia_meta.py', '') for f in all_files]
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 4: GET THE CATEGORY PATH
    # -----------------------------------------------------------------------------------------------------------------
    # eg.geography.natural_resources.natural_resources.main
    category_path = list_paths.get(category_name, '')

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 4: ESTABLIHS SET TO CAPTURE EACH UNIQUE ITEM
    # -----------------------------------------------------------------------------------------------------------------
    unique_items = set()

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 4: ITERATE OVER ALL ISO CODES
    # -----------------------------------------------------------------------------------------------------------------
    for iso_code in all_iso_codes:
        # Set category_path based on the condition for FRA and main_resources
        if iso_code == "FRA" and category_name == "main_resources":
            category_path = "geography.natural_resources.natural_resources.metropolitan_france"
        else:
            category_path = list_paths.get(category_name, '')

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # NOTE 4: COUNTRY DATA
        # -----------------------------------------------------------------------------------------------------------------
        country_data = return_country_cia_data(
            iso_code=iso_code
        )
        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # NOTE 4: ACCESS THE DATA @ categoty_path
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
                print(f"Error >> {iso_code} {iso3Code_to_cia_code().get(iso_code, {}).get('country_name','')} {iso3Code_to_cia_code().get(iso_code, {}).get('cia_code','')} {iso3Code_to_cia_code().get(iso_code, {}).get('region_name','')} >> No Data >>'{category_path}'")
                # return []
            except TypeError:
                return "Error: Non-dictionary value encountered while accessing path"
        # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        # NOTE 4: ADD THE DATA TO unique_items
        # -----------------------------------------------------------------------------------------------------------------
        if data is not None:
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, (str, int, float, tuple)):  # Ensure item is hashable
                        unique_items.add(item)
                    else:
                        print(
                            f"Error >> {iso_code}  {iso3Code_to_cia_code().get(iso_code, {}).get('country_name','')} {iso3Code_to_cia_code().get(iso_code, {}).get('cia_code','')} {iso3Code_to_cia_code().get(iso_code, {}).get('region_name','')} >> Unhashable item in list at '{category_path}': {item}")
            # Check if data itself is hashable
            elif isinstance(data, (str, int, float, tuple)):
                unique_items.add(data)
            else:
                print(
                    f"Error >> {iso_code}  {iso3Code_to_cia_code().get(iso_code, {}).get('country_name','')} {iso3Code_to_cia_code().get(iso_code, {}).get('cia_code','')} {iso3Code_to_cia_code().get(iso_code, {}).get('region_name','')}>> Unhashable data type at '{category_path}': {type(data)}")

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # CONVERT SET TO LIST
    # -----------------------------------------------------------------------------------------------------------------
    unique_items_list = list(unique_items)

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : CLEAN - all_unique_items
    # -----------------------------------------------------------------------------------------------------------------
    # Create an empty set to store unique items
    clean_unique_items_set = set()

    # Process each item in the list
    for item in unique_items_list:
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

    return all_unique_items


# ---------------------------------------------------------------------------------------------------------------
# Main Function (Entry Point)
# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # main_resources, major_aquifers, general_hazards
    category_name = "main_resources"
    # ------------------------------------------------------------------------------------------------------------
    print(
        aggregate_all_possible_items(
            category_name=category_name,
        ))
    # ------------------------------------------------------------------------------------------------------------
