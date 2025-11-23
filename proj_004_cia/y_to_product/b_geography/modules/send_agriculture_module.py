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
#   CORE IMPORTS impact_titan.impact_2_tools.f_product.d_navigate_product.impact_project_address
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
#   HELPER FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def generate_tabs_content(all_main_keys_slugified):
    """
    Generates the Svelte `Tabs.Content` block for natural_resources with dynamic conditions.
    """
    # Start of Tabs.Content block
    tabs_content = """
    <Tabs.Content value="natural_resources" class="space-y-4">
        <!-- natural_resources -->
        <main class="marble">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                {#each country_main_resources as route_data, i}
                    <Country_List_Card>
                        <div slot="icon">
    """

    # Generate the {#if} conditions for icons
    for index, key in enumerate(all_main_keys_slugified):
        icon_name = f"{key.capitalize()}_icon"
        if index == 0:
            # First condition uses {#if}
            tabs_content += f"""
                            {{#if route_data.key === '{key}'}} 
                                <Main_resources_icon_finder iconName="{icon_name}" size="70" />
            """
        elif index == len(all_main_keys_slugified) - 1:
            # Last condition uses {/if} to close
            tabs_content += f"""
                            {{:else}} 
                                <Main_resources_icon_finder iconName="Default_icon" size="70" />
                            {{/if}}
            """
        else:
            # Middle conditions use {:else if}
            tabs_content += f"""
                            {{:else if route_data.key === '{key}'}} 
                                <Main_resources_icon_finder iconName="{icon_name}" size="70" />
            """

    # End of the main div and Tabs.Content block
    tabs_content += """
                        </div>
                        <div slot="title">
                            {route_data.title}
                        </div>
                    </Country_List_Card>
                {/each}
            </div>
        </main>
    </Tabs.Content>
    """

    return tabs_content
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def send_agriculture_module(
    projectFolderName=None,
    selectedCountry=None,
):

    dest_kit_folder_name = 'a11_country_kit'
    dest_component_folder_name = 'a5_country_agriculture'

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: GET THE UNIQUE ITEMS FOR EACH LIST CATEGORY OF AGRICULTURE
    # -----------------------------------------------------------------------------------------------------------------
    all_main_resources_keys = aggregate_all_possible_items(
        category_name='main_resources',
    )

    # -----------------------------------------------------------------------------------------------------------------
    all_main_keys_slugified = [
        slugify(item, separator="_") for item in all_main_resources_keys]

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
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # Create all target folders until the target the destination
    # ---------------------------------------------------------------------------------------------------------------------
    dest_folders = impact_project_address(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,
        section_name='world',
    )
    # ------------------------------------------------------------------------------------------------------------------
    all_world_kit_folder = dest_folders['main_section_kit_folder']
    # ---------------------------------------------------------------------------------------------------------------------
    # The main kit folder in the target project
    # ---------------------------------------------------------------------------------------------------------------------
    main_kit_folder = os.path.join(all_world_kit_folder, dest_kit_folder_name)
    # ------------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------
    # Components folder
    # ---------------------------------------------------------------------------------------------------------------------
    dest_component_folder = os.path.join(
        main_kit_folder, 'components', dest_component_folder_name)
    # ---------------------------------------------------------------------------------------------------------------------
    # Create if not exists
    # ---------------------------------------------------------------------------------------------------------------------
    os.makedirs(dest_component_folder, exist_ok=True)

    # /////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: SVELTE COMPONENT CONTENT
    # ---------------------------------------------------------------------------------------------
    file_name = f'Country_agriculture.svelte'
    file_path = os.path.join(dest_component_folder, file_name)

    # Generate dynamic Tabs.Content for natural_resources
    natural_resources_content = generate_tabs_content(all_main_keys_slugified)

    # TOP HALF OF SCRIPT
    # ---------------------------------------------------------------------------------------------
    top_half = """
<script lang='ts'>

    ///////////////////////////////////////////////////////////////////////////////////////////
    // IMPORTS
    ///////////////////////////////////////////////////////////////////////////////////////////

    import { build_routes_for_list_items_at_country_key } from '$lib/Components/KitsDynamic/All_world_kit/w_system_utils/a9_cia_utils/a1_build_routes_for_list_items_at_country_key';
    import { main_resources_routes } from '$lib/Components/KitsDynamic/All_world_kit/v_route_data/a5a_cia_list_routes/main_resources_routes';
    import { main_resources_each_country } from '$lib/Components/KitsDynamic/All_world_kit/u_system_data/a9_cia_data/b_geography/main_resources_each_country';

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
    let country_main_resources = [];
    ///////////////////////////////////////////////////////////////////////////////////////////
	import { onMount } from 'svelte';
    onMount(() => {
        country_main_resources = build_routes_for_list_items_at_country_key(
            country_key,
            main_resources_each_country,
            main_resources_routes
        );
    });
    ///////////////////////////////////////////////////////////////////////////////////////////
    // REACTIVITY
    ///////////////////////////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////////////////////////////////////////
    //UI
    ///////////////////////////////////////////////////////////////////////////////////////////
    import Main_resources_icons from '$lib/Components/KitsDynamic/All_world_kit/y_icons/cia/main_resources/_main_component/Main_resources_icons.svelte'
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
    # JOIN # Combine all parts
    # ---------------------------------------------------------------------------------------------
    final_content = top_half + natural_resources_content + bottom_half
    # /////////////////////////////////////////////////////////////////////////////////////////////

    # wirte in the file
    with open(file_path, 'w') as f:
        f.write(final_content)
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
    send_agriculture_module(
        projectFolderName=projectFolderName,
        selectedCountry=selectedCountry,

    )
