'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF ECONOMY INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_economy ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_06_economy.helper.get_economy import get_economy
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   CORE FUNCTION
# --------------------------------------------------------------------------------------------------------------------


def return_economy_data(
    data: dict,
    iso3Code: str
):

    # 6. ECONOMY
    # //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # Note: 'agricultural_products'
    cia_pack['agricultural_products'] = get_economy(
        data=data, info='agricultural_products', iso3Code=iso3Code)
    # Note: 'argicultural_products_2'
    cia_pack['argicultural_products_2'] = get_economy(
        data=data, info='argicultural_products_2', iso3Code=iso3Code)
    # Note: 'average_household_exp'
    cia_pack['average_household_exp'] = get_economy(
        data=data, info='average_household_exp', iso3Code=iso3Code)
    # Note: 'budget'
    cia_pack['budget'] = get_economy(
        data=data, info='budget', iso3Code=iso3Code)
    # Note: 'budget_surplus_deficit'
    cia_pack['budget_surplus_deficit'] = get_economy(
        data=data, info='budget_surplus_deficit', iso3Code=iso3Code)
    # Note: 'credit_ratings'
    cia_pack['credit_ratings'] = get_economy(
        data=data, info='credit_ratings', iso3Code=iso3Code)
    # Note: 'economic_overview'
    cia_pack['economic_overview'] = get_economy(
        data=data, info='economic_overview', iso3Code=iso3Code)
    # Note: 'exports_commodities'
    cia_pack['exports_commodities'] = get_economy(
        data=data, info='exports_commodities', iso3Code=iso3Code)
    # Note: 'exports_partners'
    cia_pack['exports_partners'] = get_economy(
        data=data, info='exports_partners', iso3Code=iso3Code)
    # Note: 'gdp_composition_by_end_use'
    cia_pack['gdp_composition_by_end_use'] = get_economy(
        data=data, info='gdp_composition_by_end_use', iso3Code=iso3Code)
    # Note: 'gdp_composition_sector_of_origin'
    cia_pack['gdp_composition_sector_of_origin'] = get_economy(
        data=data, info='gdp_composition_sector_of_origin', iso3Code=iso3Code)
    # Note: 'gini'
    cia_pack['gini'] = get_economy(
        data=data, info='gini', iso3Code=iso3Code)
    # Note: 'household_income'
    cia_pack['household_income'] = get_economy(
        data=data, info='household_income', iso3Code=iso3Code)
    # Note: 'imports'
    cia_pack['imports'] = get_economy(
        data=data, info='imports', iso3Code=iso3Code)
    # Note: 'imports_commodities'
    cia_pack['imports_commodities'] = get_economy(
        data=data, info='imports_commodities', iso3Code=iso3Code)
    # Note: 'imports_partners'
    cia_pack['imports_partners'] = get_economy(
        data=data, info='imports_partners', iso3Code=iso3Code)
    # Note: 'industrial_production'
    cia_pack['industrial_production'] = get_economy(
        data=data, info='industrial_production', iso3Code=iso3Code)
    # Note: 'industries'
    cia_pack['industries'] = get_economy(
        data=data, info='industries', iso3Code=iso3Code)
    # Note: 'labor_force_by_occupation'
    cia_pack['labor_force_by_occupation'] = get_economy(
        data=data, info='labor_force_by_occupation', iso3Code=iso3Code)
    # Note: 'remittances'
    cia_pack['remittances'] = get_economy(
        data=data, info='remittances', iso3Code=iso3Code)
    # Note: 'reserves_of_foreign_exchange_and_gold'
    cia_pack['reserves_of_foreign_exchange_and_gold'] = get_economy(
        data=data, info='reserves_of_foreign_exchange_and_gold', iso3Code=iso3Code)
    # Note: 'youth_unemployment_rate'
    cia_pack['youth_unemployment_rate'] = get_economy(
        data=data, info='youth_unemployment_rate', iso3Code=iso3Code)

    # Return the compiled geography data
    return cia_pack


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#   TEST FUNCTION
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    import platform
    country = True
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
        return_economy_data(
            data=data,
            iso3Code=iso3Code
        )
    )
