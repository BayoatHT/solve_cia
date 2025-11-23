import os
import importlib.util
from tqdm import tqdm
from app.bkMaker.a03h_World_Manager.a0_cia_integrate.a1_lists._build.a1_list_paths import list_paths
from app.bkMaker.a03h_World_Manager.a0_cia_integrate.a1_lists._translate.a2_auto_update_list_translated_files import auto_update_list_translated_files

# ---------------------------------------------------------------------------------------------------------------
# Function to run auto_update_translated_files for each category in the section
# ---------------------------------------------------------------------------------------------------------------


def auto_update_all_cia_translations():
    """
    Auto-update translations for all categories in the given section by running auto_update_translated_files.

    Args:
        section_name (str): The name of the section to process.
    """
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: HANDLE TRANSLATION FOR LIST CATEGORIES
    # -----------------------------------------------------------------------------------------------------------------
    # Iterate over each category and translate the respective files
    for category_name in tqdm(list_paths, desc=f"Updating all Translations"):
        print(f"Updating all Translations: {category_name}")
        # Translate the routes
        auto_update_list_translated_files(category_name=category_name)
        print(f"Translated routes for {category_name}.")

    print(
        f"Updated all Translation files for CIA DATA")


# ---------------------------------------------------------------------------------------------------------------
# Main function entry point
# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    auto_update_all_cia_translations()
