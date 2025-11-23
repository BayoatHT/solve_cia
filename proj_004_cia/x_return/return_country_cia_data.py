import importlib
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def return_country_cia_data(
    iso_code=None,
):
    # Purpose:
    # ---------------------------------------------------------------------------------------------------------
    """
        Take the iso_code and return the CIA data for the country
    """
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: ESTBALISH BASE FOLDER
    # ---------------------------------------------------------------------------------------------------------
    base_folder = r'proj_004_cia._data_per_country'

    # /////////////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE 1: ESTBALISH BASE FOLDER
    # ---------------------------------------------------------------------------------------------------------
    target_file = f'{iso_code}_cia_meta'

    # Dynamically import the categories for the section
    try:
        dynamic_sections_module = importlib.import_module(
            f'{base_folder}.{target_file}'
        )
        full_nation_data = getattr(
            dynamic_sections_module, f'{target_file}', {})
    except ModuleNotFoundError as e:
        print(
            f"Error: Could not obtain the data for  - {iso_code}. {e}")
        return

    return full_nation_data


# ---------------------------------------------------------------------------------------------------------------
# Main Function (Entry Point)
# ---------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    iso_code = "USA"

    # ------------------------------------------------------------------------------------------------------------
    print(
        return_country_cia_data(
            iso_code=iso_code,
        ))
    # ------------------------------------------------------------------------------------------------------------
