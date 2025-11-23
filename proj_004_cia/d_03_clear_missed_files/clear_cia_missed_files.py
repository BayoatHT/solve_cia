import os
import importlib.util
from tqdm import tqdm
from app.bkMaker.a02_World_CIA_Manager.a1_lists._build.a1_list_paths import list_paths
from app.bkMaker.a02_World_CIA_Manager.a1_lists._translate.a3_clear_list_missed_files import clear_missed_files

# ---------------------------------------------------------------------------------------------------------------
# Function to run clear_missed_files for each category in the section
# ---------------------------------------------------------------------------------------------------------------


def clear_cia_missed_files(section_name):
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: HANDLE TRANSLATION FOR LIST CATEGORIES
    # -----------------------------------------------------------------------------------------------------------------
    # Iterate over each category and translate the respective files
    for category_name in tqdm(list_paths, desc=f"Translating category"):
        print(f"Translating category: {category_name}")
        # Translate the routes
        clear_missed_files(category_name=category_name)
        print(f"Translated routes for {category_name}.")

    print(
        f"Completed auto-clearing missed files for section: {section_name}")


# ---------------------------------------------------------------------------------------------------------------
# Main function entry point
# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    section_name = "clients"  # Example section name
    clear_cia_missed_files(section_name)
