# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
from proj_004_cia.__logger.logger import app_logger  # Centralized logger
# Retrieves project paths
# ---------------------------------------------------------------------------------------------------------------------
from impact_titan.impact_6_product.e_world_system.e_0_set_up.b1_shared_in_system import shared_in_system
from proj_004_cia.y_to_product.a_send_all_list_category_data import send_all_list_category_data
from impact_titan.impact_6_product.e_world_system._world_manager.x3PageData.send.utils.a0_create_dest_world_system_data_folder import create_dest_world_system_data_folder
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------


def send_cia_data(
        projectFolderName: str = None,
        selectedCountry: dict = None,
):

    # Log the start of the process
    # ------------------------------------------------------------------------------------------------------
    app_logger.info(
        f"Starting TRANSFER OF ALL WORLD SYSTEM DATA - WORLD CUSTOM TOPICS @ {projectFolderName}."
    )

    # STEP 2: Retrieve project paths
    # ------------------------------------------------------------------------------------------------------
    try:

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
            impact_world_data_folder, dest_data_folder_name)
        # --------------------------------------------------------------------------------------------------
        # Create destination folder
        # --------------------------------------------------------------------------------------------------
        os.makedirs(dest_folder, exist_ok=True)

    except Exception as e:
        app_logger.error(
            f"Error retrieving project paths for world system data': {e}")
        return

    # STEP 3: Create main section kit folder and its components
    try:

        # --------------------------------------------------------------------------------------------------
        # Send the world topics data
        # --------------------------------------------------------------------------------------------------
        send_all_list_category_data(
            projectFolderName=projectFolderName,
            selectedCountry=selectedCountry,
        )

    except Exception as e:
        app_logger.error(
            f"Error while running the transfer of world system data - WORLD CUSTOM TOPICS folder: {e}"
        )
        return


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    # Test configuration
    projectFolderName = 'Main_en'
    selectedCountry = {
        "countryCode": "MAIN",
        "name": "Impact Titan - Admin Default",
        "region": "Default",
        "internet_code": ".com",
        "languageCode": "en",
        "selectedLanguage": "English"
    }
    # ---------------------------------------------------------------------------------------------------------------------
    # Execute the function
    send_cia_data(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )
