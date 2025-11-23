######################################################################################################################
# CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------

from proj_004_cia.c_00_transform_utils.clean_text import clean_text


def get_introduction(data: dict, info: str, iso3Code: str) -> str:
    """
    Retrieve the introduction background text from the data.

    Parameters:
    - data: The dictionary containing the country's data.
    - info: The specific information to retrieve (should be 'background' for this function).
    - iso3Code: The ISO3 code of the country.

    Returns:
    - A string containing the cleaned background text.
    """
    if info != 'background':
        return ''

    # Access the background text safely
    background_info = data.get("Introduction", {}).get("Background", {})
    text = background_info.get('text', '')

    # Handle cases where text might not be available
    if not text:
        print(f"Warning: No background text found for {iso3Code}")
        return ''

    # Clean the text
    cleaned_text = clean_text(text)

    return cleaned_text


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    from pprint import pprint
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data
    # --------------------------------------------------------------------------------------------------
    info = 'pass'  # Change this to test specific fields
    iso3Code = 'USA'  # Change to any ISO3 code: 'USA', 'FRA', 'WLD', 'DEU', etc.
    # --------------------------------------------------------------------------------------------------
    data = load_country_data(iso3Code)
    # --------------------------------------------------------------------------------------------------
    pprint(get_introduction(data=data, info=info, iso3Code=iso3Code))
