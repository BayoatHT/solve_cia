# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
import importlib
# ----------------------------------------------------------------------------------------------------------------------
from impact_titan.impact_6_product.e_world_system.e_0_set_up.b1_shared_in_system import shared_in_system
from impact_titan.impact_6_product.e_world_system._world_manager.x3PageData.send.utils.a0_create_dest_world_system_data_folder import create_dest_world_system_data_folder
# ----------------------------------------------------------------------------------------------------------------------

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION impact_titan.impact_6_product.e_world_system.e_0_set_up
# ---------------------------------------------------------------------------------------------------------------------


def send_natural_resources_per_country(
    projectFolderName=None,
    selectedCountry=None,

):

    list_category_name = "main_resources"
    # DESTINATION
    # ------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    # Create all target folders until the target the destination
    # --------------------------------------------------------------------------------------------------
    impact_world_data_folder = create_dest_world_system_data_folder(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )
    # --------------------------------------------------------------------------------------------------
    # group destination folder
    # --------------------------------------------------------------------------------------------------
    dest_data_folder_name = shared_in_system.get('data').get(
        'sub_groups').get('cia_data').get('dest')
    dest_folder = os.path.join(
        impact_world_data_folder, dest_data_folder_name, 'b_geography', 'main_resources')
    # --------------------------------------------------------------------------------------------------
    # Create destination folder
    # --------------------------------------------------------------------------------------------------
    os.makedirs(dest_folder, exist_ok=True)

    # ACCESS THE DATA
    # ------------------------------------------------------------------------------------------------------------------
    # Dynamically import the categories for the section
    # ------------------------------------------------------------------------------------------------------------------
    try:
        dynamic_sections_module = importlib.import_module(
            f'proj_004_cia._data_per_category.b_geography.{list_category_name}.list_each_country.{list_category_name}_each_country'
        )
        list_data = getattr(
            dynamic_sections_module, f'{list_category_name}_keys', {})
    except ModuleNotFoundError as e:
        print(
            f"Error: Could not import each country list data '{list_category_name}'. {e}")
        return

    # ------------------------------------------------------------------------------------------------------------------

    # ACCESS THE DATA TYPE
    # -------------------------------------------------------------------------------------------------------------------
    list_data_type_name = f'List_data_type'
    list_data_type = """
// ESTBLISH TYPE FOR COUNTRY REGIONS
export type List_data_type  = {
    [countryCode: string]: string[];
};
    """

    # Write the content to the file
    # --------------------------------------------------------------------------------------------------------------------
    variable_name = f'{list_category_name}_each_country'
    file_name = f'{variable_name}.ts'
    file_path = os.path.join(dest_folder, file_name)
    # --------------------------------------------------------------------------------------------------------------------

    # Write the content to the file
    # --------------------------------------------------------------------------------------------------------------------
    with open(file_path, 'w', encoding='utf-8') as file:
        # -----------------------------------------------------------------------------------------------------------------
        # ESTABLISH TYPE BASE COUNTRY META DATA
        # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        file.write("// ESTBLISH TYPE\n")
        file.write(list_data_type)
        file.write("\n\n")
        # ESTABLISH DATA
        # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        file.write("\n\n// ESTBLISH DATA\n")
        file.write(
            f'\n\nexport const {variable_name}: {list_data_type_name} = ')
        json.dump(list_data, file, ensure_ascii=False, indent=4)

    # -----------------------------------------------------------------------------------------------------------------
    # PRINT SUCCESS MESSAGE
    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    print(f"{list_category_name} - Country keys array file generated for {projectFolderName}.")

    # -----------------------------------------------------------------------------------------------------------------
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    projectFolderName = 'Main_en'
    selectedCountry = {
        "countryCode": "MAIN",
        "name": "Impact Titan - Admin Default",
        "region": "Default",
        "internet_code": ".com",
        "languageCode": "en",
        "selectedLanguage": "English"
    }
    # -----------------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------------
    send_natural_resources_per_country(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )
