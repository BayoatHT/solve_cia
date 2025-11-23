# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
import importlib
# ----------------------------------------------------------------------------------------------------------------------
from impact_titan.impact_2_tools.f_product.d_navigate_product.impact_project_address import impact_project_address

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def send_list_for_each_country(
    projectFolderName=None,
    selectedCountry=None,
    list_category_name=None,
):

    # DESTINATION
    # ------------------------------------------------------------------------------------------------------------------
    # Generate folder paths based on project folder name and country
    targetFolders = impact_project_address(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )
    # ------------------------------------------------------------------------------------------------------------------
    cia_data_folder = targetFolders["cia_data_folder"]
    # ------------------------------------------------------------------------------------------------------------------
    dest_folder = os.path.join(
        cia_data_folder, 'country_list_folder', 'function')
    os.makedirs(dest_folder, exist_ok=True)
    # ------------------------------------------------------------------------------------------------------------------

    function_script = """
type CountryKey = string

interface CountryList {
	[key: string]: string[]
}

interface Route {
	title: string
	slug: string
	route: string
	desc: string
	key: string
}

interface Routes {
	[key: string]: Route
}

/**
 * Function to return a list of routes based on the provided country key and data.
 * @param countryKey - The key representing a country (e.g., "NGA").
 * @param eachCountryList - An object containing country keys and their respective lists.
 * @param routes - An object containing route data.
 * @returns An array of route objects that match the properties in the routes data.
 */
export function return_list_of_routes(
	countryKey: CountryKey,
	eachCountryList: CountryList,
	routes: Routes
): Route[] {
	// Check if the countryKey exists in the eachCountryList
	const countryResources = eachCountryList[countryKey]

	// If countryKey is not found, return an empty array
	if (!countryResources) {
		return []
	}

	// Initialize an array to store matching routes
	const matchedRoutes: Route[] = []

	// Loop through each resource for the country
	for (const resource of countryResources) {
		// Check if the resource exists in the routes data
		if (routes[resource]) {
			// Add the matching route object to the result array
			matchedRoutes.push(routes[resource])
		}
	}

	// Return the list of matched routes
	return matchedRoutes
}

    """
    # Write the content to the file
    # --------------------------------------------------------------------------------------------------------------------
    variable_name = f'return_list_of_routes'
    file_name = f'{variable_name}.ts'
    file_path = os.path.join(dest_folder, file_name)
    # --------------------------------------------------------------------------------------------------------------------

    # Write the content to the file
    # --------------------------------------------------------------------------------------------------------------------
    with open(file_path, 'w', encoding='utf-8') as file:
        # -----------------------------------------------------------------------------------------------------------------
        # ESTABLISH TYPE BASE COUNTRY META DATA
        # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        file.write("// USED TO RETURN LIST ROUTE DATA PER COUNTRY \n\n")
        file.write(function_script)
        file.write("\n\n")

    # -----------------------------------------------------------------------------------------------------------------
    # PRINT SUCCESS MESSAGE
    # ////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    print(f"{list_category_name.upper()} - function file generated for {projectFolderName}.")


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
    list_category_name = "main_resources"
    # -----------------------------------------------------------------------------------------------------------------------
    send_list_for_each_country(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
        list_category_name=list_category_name
    )
