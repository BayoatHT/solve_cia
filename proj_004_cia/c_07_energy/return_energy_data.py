'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF ENERGY INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_energy ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_07_energy.helper.get_energy import get_energy

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------


def return_energy_data(
    data: dict,
    iso3Code: str
):

    # 7. energy
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # Conditional inclusion based on iso3Code
    if iso3Code != 'WLD':
        # Note: 'carbon_dioxide_emissions'
        cia_pack['carbon_dioxide_emissions'] = get_energy(
            data=data, info='carbon_dioxide_emissions', iso3Code=iso3Code)
        # Note: 'carbon_dioxide_from_consumption'
        cia_pack['carbon_dioxide_from_consumption'] = get_energy(
            data=data, info='carbon_dioxide_from_consumption', iso3Code=iso3Code)
        # Note: 'coal'
        cia_pack['coal'] = get_energy(
            data=data, info='coal', iso3Code=iso3Code)
        # Note: 'crude_oil_exports'
        cia_pack['crude_oil_exports'] = get_energy(
            data=data, info='crude_oil_exports', iso3Code=iso3Code)
        # Note: 'crude_oil_imports'
        cia_pack['crude_oil_imports'] = get_energy(
            data=data, info='crude_oil_imports', iso3Code=iso3Code)
        # Note: 'crude_oil_production'
        cia_pack['crude_oil_production'] = get_energy(
            data=data, info='crude_oil_production', iso3Code=iso3Code)
        # Note: 'crude_oil_proved_reserves'
        cia_pack['crude_oil_proved_reserves'] = get_energy(
            data=data, info='crude_oil_proved_reserves', iso3Code=iso3Code)
        # Note: 'electricity'
        cia_pack['electricity'] = get_energy(
            data=data, info='electricity', iso3Code=iso3Code)
        # Note: 'electricity_consumption'
        cia_pack['electricity_consumption'] = get_energy(
            data=data, info='electricity_consumption', iso3Code=iso3Code)
        # Note: 'electricity_exports'
        cia_pack['electricity_exports'] = get_energy(
            data=data, info='electricity_exports', iso3Code=iso3Code)
        # Note: 'electricity_from_fossil'
        cia_pack['electricity_from_fossil'] = get_energy(
            data=data, info='electricity_from_fossil', iso3Code=iso3Code)
        # Note: 'electricity_from_hydro'
        cia_pack['electricity_from_hydro'] = get_energy(
            data=data, info='electricity_from_hydro', iso3Code=iso3Code)
        # Note: 'electricity_from_nuclear'
        cia_pack['electricity_from_nuclear'] = get_energy(
            data=data, info='electricity_from_nuclear', iso3Code=iso3Code)
        # Note: 'electricity_imports'
        cia_pack['electricity_imports'] = get_energy(
            data=data, info='electricity_imports', iso3Code=iso3Code)
        # Note: 'electricity_from_other_renewable'
        cia_pack['electricity_from_other_renewable'] = get_energy(
            data=data, info='electricity_from_other_renewable', iso3Code=iso3Code)
        # Note: 'electricity_generating_capacity'
        cia_pack['electricity_generating_capacity'] = get_energy(
            data=data, info='electricity_generating_capacity', iso3Code=iso3Code)
        # Note: 'electricity_production'
        cia_pack['electricity_production'] = get_energy(
            data=data, info='electricity_production', iso3Code=iso3Code)
        # Note: 'electricity_access'
        cia_pack['electricity_access'] = get_energy(
            data=data, info='electricity_access', iso3Code=iso3Code)
        # Note: 'electricity_sources'
        cia_pack['electricity_sources'] = get_energy(
            data=data, info='electricity_sources', iso3Code=iso3Code)
        # Note: 'energy_consumption_per_capita'
        cia_pack['energy_consumption_per_capita'] = get_energy(
            data=data, info='energy_consumption_per_capita', iso3Code=iso3Code)
        # Note: 'natural_gas'
        cia_pack['natural_gas'] = get_energy(
            data=data, info='natural_gas', iso3Code=iso3Code)
        # Note: 'natural_gas_consumption'
        cia_pack['natural_gas_consumption'] = get_energy(
            data=data, info='natural_gas_consumption', iso3Code=iso3Code)
        # Note: 'natural_gas_exports'
        cia_pack['natural_gas_exports'] = get_energy(
            data=data, info='natural_gas_exports', iso3Code=iso3Code)
        # Note: 'natural_gas_imports'
        cia_pack['natural_gas_imports'] = get_energy(
            data=data, info='natural_gas_imports', iso3Code=iso3Code)
        # Note: 'natural_gas_production'
        cia_pack['natural_gas_production'] = get_energy(
            data=data, info='natural_gas_production', iso3Code=iso3Code)
        # Note: 'natural_gas_proved_reserves'
        cia_pack['natural_gas_proved_reserves'] = get_energy(
            data=data, info='natural_gas_proved_reserves', iso3Code=iso3Code)
        # Note: 'nuclear_energy'
        cia_pack['nuclear_energy'] = get_energy(
            data=data, info='nuclear_energy', iso3Code=iso3Code)
        # Note: 'petroleum'
        cia_pack['petroleum'] = get_energy(
            data=data, info='petroleum', iso3Code=iso3Code)
        # Note: 'refined_petroleum_consumption'
        cia_pack['refined_petroleum_consumption'] = get_energy(
            data=data, info='refined_petroleum_consumption', iso3Code=iso3Code)
        # Note: 'refined_petroleum_exports'
        cia_pack['refined_petroleum_exports'] = get_energy(
            data=data, info='refined_petroleum_exports', iso3Code=iso3Code)
        # Note: 'refined_petroleum_imports'
        cia_pack['refined_petroleum_imports'] = get_energy(
            data=data, info='refined_petroleum_imports', iso3Code=iso3Code)
        # Note: 'refined_petroleum_production'
        cia_pack['refined_petroleum_production'] = get_energy(
            data=data, info='refined_petroleum_production', iso3Code=iso3Code)
    else:
        # Note: ''
        pass

    # Return the compiled energy data
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    import platform
    country = False
    # ----------------------------------------------------------------------------------------------------------------------------------
    if platform.system() == 'Windows':
        json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
    else:
        json_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), '_raw_data')
    if country:
        region_folder = f'north-america'
        cia_code = 'us'
    else:
        region_folder = f'world'
        cia_code = 'xx'
    file_path = os.path.join(json_folder, region_folder, f'{cia_code}.json')
    # --------------------------------------------------------------------------------------------------
    with open(file_path, 'r', encoding='utf-8') as country_file:
        data = json.load(country_file)
    # --------------------------------------------------------------------------------------------------
    if country:
        iso3Code = 'USA'
    else:
        iso3Code = 'WLD'
    # ------------------------------------------------------------------------------------------------------------------
    print(
        return_energy_data(
            data=data,
            iso3Code=iso3Code
        )
    )
