from proj_004_cia.a_02_cia_area_codes.utils.cia_code_names import cia_code_names

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def iso3Code_to_cia_code():
    """
    Maps each ISO3 code in cia_code_names to a dictionary with 'region_name' and 'cia_code'.

    Returns:
        dict: A dictionary where keys are ISO3 codes, and values are dictionaries with 'region_name' and 'cia_code'.
    """
    iso3_to_cia = {}

    for parent_key, details in cia_code_names.items():
        iso3_code = details.get("iso3Code")
        region_name = details.get("region_name")
        country_name = details.get("country_name")
        if iso3_code:
            iso3_to_cia[iso3_code] = {
                "country_name": country_name,
                "region_name": region_name,
                "cia_code": parent_key
            }

    return iso3_to_cia


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    result = iso3Code_to_cia_code()
    print(result["KEN"])
