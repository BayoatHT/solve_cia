from tqdm import tqdm
from app.bkMaker.a02_World_CIA_Manager.a1_lists._build.a1_list_paths import list_paths
from app.bkMaker.a02_World_CIA_Manager.a1_lists._translate.a1_translate_list_routes import translate_list_routes


# Base folder paths
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
BASE_LEADS_FOLDER = 'C:/Users/bayoa/Desktop/bkProjects/bkManager/app/    projectFolderName = "Main_en"/_Leads'


def translate_all_cia():
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: HANDLE TRANSLATION FOR LIST CATEGORIES
    # -----------------------------------------------------------------------------------------------------------------
    # Iterate over each category and translate the respective files
    for category_name in tqdm(list_paths, desc=f"Translating category"):
        print(f"Translating category: {category_name}")
        # Translate the routes
        translate_list_routes(category_name=category_name)
        print(f"Translated routes for {category_name}.")

    print(
        f"Translation of all list categories from CIA")


# ---------------------------------------------------------------------------------------------------------------
# Main Function (Entry Point)
# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    translate_all_cia()
