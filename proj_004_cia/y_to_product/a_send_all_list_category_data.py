# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.__logger.logger import app_logger  # Centralized logger
# ----------------------------------------------------------------------------------------------------------------------
from proj_004_cia.y_to_product.b_geography.data.lists.send_natural_resources_per_country import send_natural_resources_per_country

# /////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# -----------------------------------------------------------------------------------------------------


def send_all_list_category_data(
    projectFolderName=None,
    selectedCountry=None,
):

    # Log the start of the process
    # ---------------------------------------------------------------------------------------------------------------------
    app_logger.info(
        f"Starting to transfer all cia list data - CIA DATA@ {projectFolderName}."
    )

    # cia_list_categories = list(list_paths.keys())
    cia_list_categories = ["main_resources"]

    # SEND ALL LISTS FOR EACH COUNTRY
    # ------------------------------------------------------------------------------------------------------------------
    send_natural_resources_per_country(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )


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
    send_list_for_each_country(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )
