'''
    #   PURPOSE OF THIS FILE

    NOTE:
        1. SEND ENTIRE COMPONENET FOR AGRICULTURE
        2. TAKES CARE OF THE SVELTE CONDITION FOR EACH Natural resource icon and key
        3. TAKES CARE OF THE SVELTE CONDITION FOR EACH Natural hazards icon and key
        4. TAKES CARE OF THE SVELTE CONDITION FOR EACH Major aquifer icon and key
'''


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import importlib
from impact_titan.impact_2_tools.f_product.d_navigate_product.impact_project_address import impact_project_address
from app.bkMaker.a03__Central_Page_Manager.__head_of_content.b_routes.a_routes.b1_return_category_routes import return_category_routes
# ----------------------------------------------------------------------------------------------------------------------
from slugify import slugify
from app.bkMaker.a03h_World_Manager.a0_cia_integrate.a1_lists._build.a1_list_paths import list_paths
from app.bkMaker.a03h_World_Manager.a0_cia_integrate.a1_lists._build.a2_aggregate_all_possibile_items import aggregate_all_possible_items
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def send_list_icon_main_component(
    projectFolderName=None,
    selectedCountry=None,
):

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: GET THE UNIQUE ITEMS FOR EACH LIST CATEGORY OF AGRICULTURE
    # -----------------------------------------------------------------------------------------------------------------
    all_main_resources_keys = aggregate_all_possible_items(
        category_name='main_resources',
    )

    # -----------------------------------------------------------------------------------------------------------------
    all_main_keys_slugified = [
        slugify(item, separator="_") for item in all_main_resources_keys]
    print(all_main_keys_slugified)
    """
    all_natural_hazards_keys = aggregate_all_possible_items(
        category_name='natural_hazards',
    )
    all_major_aquifers_keys = aggregate_all_possible_items(
        category_name='major_aquifers',
    )
    """

    # DESTINATION
    # ------------------------------------------------------------------------------------------------------------------
    # Generate folder paths based on project folder name and country
    targetFolders = impact_project_address(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
    )
    # ------------------------------------------------------------------------------------------------------------------
    world_components_folder = targetFolders["world_components_folder"]
    # ------------------------------------------------------------------------------------------------------------------
    dest_folder = os.path.join(
        world_components_folder, 'WorldKits', 'World_11_Country_Kit', 'Agriculture_Module')
    os.makedirs(dest_folder, exist_ok=True)
    # ------------------------------------------------------------------------------------------------------------------

    # /////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: SVELTE COMPONENT CONTENT
    # ---------------------------------------------------------------------------------------------
    file_name = f'Agriculture_module.svelte'
    file_path = os.path.join(dest_folder, file_name)

    # TOP HALF OF SCRIPT
    # ---------------------------------------------------------------------------------------------
    top_half = """
<script lang='ts'>

    ///////////////////////////////////////////////////////////////////////////////////////////
    // IMPORTS
    ///////////////////////////////////////////////////////////////////////////////////////////
    import { main_resources_each_country } from '$lib/x09Cia/country_list_folder/data/main_resources_each_country';
    import { main_resources_routes } from '$lib/x09Cia/country_list_folder/route_data/main_resources_routes';
    import { return_list_of_routes } from '$lib/x09Cia/country_list_folder/function/return_list_of_routes';
    ///////////////////////////////////////////////////////////////////////////////////////////
    //PROPS
    ///////////////////////////////////////////////////////////////////////////////////////////
    export let country_key: string = 'NGA';
    ///////////////////////////////////////////////////////////////////////////////////////////
    //FUNCTIONS
    ///////////////////////////////////////////////////////////////////////////////////////////
    //
    ///////////////////////////////////////////////////////////////////////////////////////////
    // KEY VARIABLES
    ///////////////////////////////////////////////////////////////////////////////////////////
	import { onMount } from 'svelte';
    let country_main_resources = [];
    ///////////////////////////////////////////////////////////////////////////////////////////

    onMount(() => {
        country_main_resources = return_list_of_routes(
            country_key,
            main_resources_each_country,
            main_resources_routes
        );
    });
    ///////////////////////////////////////////////////////////////////////////////////////////
    // REACTIVITY
    ///////////////////////////////////////////////////////////////////////////////////////////
    let natural_resources_title: string = 'Natural Resources';
    let major_aquifers_title: string = 'Major Aquifers';
    let general_hazards_title: string = 'General Hazards';

    ///////////////////////////////////////////////////////////////////////////////////////////
    //UI
    ///////////////////////////////////////////////////////////////////////////////////////////
    import Main_resources_icon_finder from '$lib/x09Cia/country_list_folder/icons/main_resources/main_component/Main_resources_icon_finder.svelte'
    import Country_List_Card from '$lib/Components/WorldComponents/WorldKits/World_11_Country_Kit/Partials/Country_List_Card.svelte'
    ///////////////////////////////////////////////////////////////////////////////////////////
    import * as Tabs from '$lib/Components/Shadcn/ui/tabs'
    ///////////////////////////////////////////////////////////////////////////////////////////
</script>

<Tabs.Root value="natural_resources" class="space-y-4 ">
	<Tabs.List class='grid grid-cols-2 md:grid-cols-3 h-24 md:h-20 smooth_bg rounded-md md:rounded-lg text-base mb-8'>
		<Tabs.Trigger class="h-full text-lg" value="natural_resources">{natural_resources_title}</Tabs.Trigger>
		<Tabs.Trigger class="h-full text-lg" value="major_aquifers">{major_aquifers_title}</Tabs.Trigger>
		<Tabs.Trigger class="h-full text-lg" value="general_hazards">{general_hazards_title}</Tabs.Trigger>
	</Tabs.List>
    """

    # BOTTOM HALF OF SCRIPT
    # ---------------------------------------------------------------------------------------------
    bottom_half = """
    
	<Tabs.Content value="major_aquifers" class="space-y-4">
		<!-- major_aquifers -->
	</Tabs.Content>

	<Tabs.Content value="general_hazards" class="space-y-4">
		<!-- general_hazards -->
	</Tabs.Content>

</Tabs.Root>
    """

    # /////////////////////////////////////////////////////////////////////////////////////////////
    # JOIN
    # ---------------------------------------------------------------------------------------------
    finalIconComponentContent = top_half + bottom_half
    # /////////////////////////////////////////////////////////////////////////////////////////////

    # wirte in the file
    with open(file_path, 'w') as f:
        f.write(finalIconComponentContent)
        print(
            f'Agriculture Module component written to {projectFolderName}')


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
    send_list_icon_main_component(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,

    )
