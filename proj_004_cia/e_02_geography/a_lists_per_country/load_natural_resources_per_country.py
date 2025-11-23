#######################################################################################################################
# proj_004_cia\e_02_geography\a_lists_per_country\load_natural_resources_per_country.py
# ---------------------------------------------------------------------------------------------------------------------


#######################################################################################################################
# CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
from proj_004_cia.e_00_load_utils.a_lists.a3_return_list_for_each_country import return_list_for_each_country


#######################################################################################################################
# UTILITY FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------
def load_natural_resources_per_country():
    """
    Returns a list of natural resources for each country.
    :return: List of natural resources for each country
    """
    category_name = "main_resources"
    # -----------------------------------------------------------------------------------------------------------------
    natural_resources_per_country = return_list_for_each_country(
        category_name=category_name,
    )
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : DESTINATION - Each Country FOLDER C:\\Users\\bayoa\\impact_projects\\claude_solve_cia\\proj_004_cia\\_data_per_category
    # --------------------------------------------------------------------------------------------------
    base_folder = r'C:\\Users\\bayoa\\impact_projects\\claude_solve_cia\\proj_004_cia\\_data_per_category'
    each_country_folder = f'{base_folder}/b_geography/{category_name}/list_each_country'
    os.makedirs(each_country_folder, exist_ok=True)
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE : DESTINATION ESTABLISH FILE NAME
    # -----------------------------------------------------------------------------------------------------------------
    # Path to the each file for the category
    each_file = os.path.join(
        each_country_folder, f'{category_name}_each_country.py')
    # /////////////////////////////////////////////////////////////////////////////////////////////#
    # NOTE : WRITE TO FILE
    # --------------------------------------------------------------------------------------------------
    with open(each_file, 'w') as file:
        file.write(
            f"{category_name}_keys = {json.dumps(natural_resources_per_country, indent=4)}\n")

    # /////////////////////////////////////////////////////////////////////////////////////////////#
    # NOTE : CONFIRMATION MESSAGE
    # --------------------------------------------------------------------------------------------------
    return f'{category_name} >>> Loacded Country list for list cia categories have been generated'


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    category_name = "main_resources"
    # -----------------------------------------------------------------------------------------------------------------
    print(load_natural_resources_per_country())
