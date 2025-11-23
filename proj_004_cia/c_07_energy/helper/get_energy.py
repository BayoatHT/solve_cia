######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import json
import logging
# NOTE: "Carbon dioxide emissions"
from proj_004_cia.c_07_energy.helper.utils.parse_carbon_dioxide_emissions import parse_carbon_dioxide_emissions
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Carbon dioxide emissions from consumption of energy"
from proj_004_cia.c_07_energy.helper.utils.parse_carbon_dioxide_from_consumption import parse_carbon_dioxide_from_consumption
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Coal"
from proj_004_cia.c_07_energy.helper.utils.parse_coal import parse_coal
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Crude oil - exports"
from proj_004_cia.c_07_energy.helper.utils.parse_crude_oil_exports import parse_crude_oil_exports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Crude oil - imports"
from proj_004_cia.c_07_energy.helper.utils.parse_crude_oil_imports import parse_crude_oil_imports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Crude oil - production"
from proj_004_cia.c_07_energy.helper.utils.parse_crude_oil_production import parse_crude_oil_production
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Crude oil - proved reserves"
from proj_004_cia.c_07_energy.helper.utils.parse_crude_oil_proved_reserves import parse_crude_oil_proved_reserves
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity import parse_electricity
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - consumption"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_consumption import parse_electricity_consumption
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - exports"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_exports import parse_electricity_exports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - from fossil fuels"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_from_fossil import parse_electricity_from_fossil
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - from hydroelectric plants"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_from_hydro import parse_electricity_from_hydro
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - from nuclear fuels"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_from_nuclear import parse_electricity_from_nuclear
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - from other renewable sources"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_from_other_renewable import parse_electricity_from_other_renewable
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - imports"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_imports import parse_electricity_imports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - installed generating capacity"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_generating_capacity import parse_electricity_generating_capacity
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity - production"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_production import parse_electricity_production
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity access"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_access import parse_electricity_access
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Electricity generation sources"
from proj_004_cia.c_07_energy.helper.utils.parse_electricity_sources import parse_electricity_sources
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Energy consumption per capita"
from proj_004_cia.c_07_energy.helper.utils.parse_energy_consumption_per_capita import parse_energy_consumption_per_capita
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Natural gas"
from proj_004_cia.c_07_energy.helper.utils.parse_natural_gas import parse_natural_gas
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Natural gas - consumption"
from proj_004_cia.c_07_energy.helper.utils.parse_natural_gas_consumption import parse_natural_gas_consumption
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Natural gas - exports"
from proj_004_cia.c_07_energy.helper.utils.parse_natural_gas_exports import parse_natural_gas_exports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Natural gas - imports"
from proj_004_cia.c_07_energy.helper.utils.parse_natural_gas_imports import parse_natural_gas_imports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Natural gas - production"
from proj_004_cia.c_07_energy.helper.utils.parse_natural_gas_production import parse_natural_gas_production
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Natural gas - proved reserves"
from proj_004_cia.c_07_energy.helper.utils.parse_natural_gas_proved_reserves import parse_natural_gas_proved_reserves
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Nuclear energy"
from proj_004_cia.c_07_energy.helper.utils.parse_nuclear_energy import parse_nuclear_energy
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Petroleum"
from proj_004_cia.c_07_energy.helper.utils.parse_petroleum import parse_petroleum
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Refined petroleum products - consumption"
from proj_004_cia.c_07_energy.helper.utils.parse_refined_petroleum_consumption import parse_refined_petroleum_consumption
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Refined petroleum products - exports"
from proj_004_cia.c_07_energy.helper.utils.parse_refined_petroleum_exports import parse_refined_petroleum_exports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Refined petroleum products - imports"
from proj_004_cia.c_07_energy.helper.utils.parse_refined_petroleum_imports import parse_refined_petroleum_imports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Refined petroleum products - production"
from proj_004_cia.c_07_energy.helper.utils.parse_refined_petroleum_production import parse_refined_petroleum_production
# --------------------------------------------------------------------------------------------------


# //////////////////////////////////////////////////////////////////////////////////////////////////


def get_energy(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: ENERGY DATA
    # --------------------------------------------------------------------------------------------------
    energy_data = data.get("Energy", {})
    # --------------------------------------------------------------------------------------------------

    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'Carbon dioxide emissions'
    # --------------------------------------------------------------------------------------------------
    carbon_dioxide_emissions_data = energy_data.get(
        "Carbon dioxide emissions", {})

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'carbon_dioxide_emissions':
        return parse_carbon_dioxide_emissions(
            carbon_dioxide_emissions_data
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'Carbon dioxide emissions from consumption of energy'
    # --------------------------------------------------------------------------------------------------
    co2_emissions_energy_consumption_data = energy_data.get(
        "Carbon dioxide emissions from consumption of energy", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'carbon_dioxide_from_consumption':
        return parse_carbon_dioxide_from_consumption(
            co2_emissions_energy_consumption_data
        )

    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'Coal'
    # --------------------------------------------------------------------------------------------------
    coal_data = energy_data.get("Coal", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'coal':
        return parse_coal(
            coal_data
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'Crude oil - exports'
    # --------------------------------------------------------------------------------------------------
    crude_oil_exports_data = energy_data.get("Crude oil - exports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'crude_oil_exports':
        return parse_crude_oil_exports(
            crude_oil_exports_data
        )

    # 5
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'Crude oil - imports'
    # --------------------------------------------------------------------------------------------------
    crude_oil_imports_data = energy_data.get("Crude oil - imports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'crude_oil_imports':
        return parse_crude_oil_imports(
            crude_oil_imports_data
        )

    # 6
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'Crude oil - production'
    # --------------------------------------------------------------------------------------------------
    crude_oil_production_data = energy_data.get("Crude oil - production", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'crude_oil_production':
        return parse_crude_oil_production(
            crude_oil_production_data
        )

    # 7
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7 >>> 'Crude oil - proved reserves'
    # --------------------------------------------------------------------------------------------------
    crude_oil_proved_reserves_data = energy_data.get(
        "Crude oil - proved reserves", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'crude_oil_proved_reserves':
        return parse_crude_oil_proved_reserves(
            crude_oil_proved_reserves_data
        )

    # 8
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 8 >>> 'Electricity'
    # --------------------------------------------------------------------------------------------------
    electricity_data = energy_data.get("Electricity", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity':
        return parse_electricity(
            electricity_data
        )

    # 9
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 9 >>> 'Electricity - consumption'
    # --------------------------------------------------------------------------------------------------
    electricity_consumption_data = energy_data.get(
        "Electricity - consumption", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_consumption':
        return parse_electricity_consumption(
            electricity_consumption_data
        )

    # 10
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 10 >>> 'Electricity - exports'
    # --------------------------------------------------------------------------------------------------
    electricity_exports_data = energy_data.get("Electricity - exports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_exports':
        return parse_electricity_exports(
            electricity_exports_data
        )

    # 11
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 11 >>> 'Electricity - from fossil fuels'
    # --------------------------------------------------------------------------------------------------
    electricity_fossil_fuels_data = energy_data.get(
        "Electricity - from fossil fuels", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_from_fossil':
        return parse_electricity_from_fossil(
            electricity_fossil_fuels_data
        )

    # 12
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 12 >>> 'Electricity - from hydroelectric plants'
    # --------------------------------------------------------------------------------------------------
    electricity_hydroelectric_data = energy_data.get(
        "Electricity - from hydroelectric plants", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_from_hydro':
        return parse_electricity_from_hydro(
            electricity_hydroelectric_data
        )

    # 13
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'Electricity - from nuclear fuels'
    # --------------------------------------------------------------------------------------------------
    electricity_nuclear_fuels_data = energy_data.get(
        "Electricity - from nuclear fuels", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_from_nuclear':
        return parse_electricity_from_nuclear(
            electricity_nuclear_fuels_data
        )
    # 14
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 14 >>> 'Electricity - from other renewable sources'
    # --------------------------------------------------------------------------------------------------
    electricity_renewable_sources_data = energy_data.get(
        "Electricity - from other renewable sources", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_imports':
        return parse_electricity_from_other_renewable(
            electricity_renewable_sources_data
        )

    # 15
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 15 >>> 'Electricity - imports'
    # --------------------------------------------------------------------------------------------------
    electricity_imports_data = energy_data.get("Electricity - imports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_imports':
        return parse_electricity_imports(
            electricity_imports_data
        )

    # 16
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 16 >>> 'Electricity - installed generating capacity'
    # --------------------------------------------------------------------------------------------------
    electricity_generating_capacity_data = energy_data.get(
        "Electricity - installed generating capacity", {})

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_generating_capacity':
        return parse_electricity_generating_capacity(
            electricity_generating_capacity_data
        )

    # 17
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 17 >>> 'Electricity - production'
    # --------------------------------------------------------------------------------------------------
    electricity_production_data = energy_data.get(
        "Electricity - production", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_production':
        return parse_electricity_production(
            electricity_production_data
        )

    # 18
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 18 >>> 'Electricity access'
    # --------------------------------------------------------------------------------------------------
    electricity_access_data = energy_data.get("Electricity access", {})

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_access':
        return parse_electricity_access(
            electricity_access_data
        )

    # 19
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 19 >>> 'Electricity generation sources'
    # --------------------------------------------------------------------------------------------------
    electricity_generation_sources_data = energy_data.get(
        "Electricity generation sources", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'electricity_sources':
        return parse_electricity_sources(
            electricity_generation_sources_data
        )

    # 20
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 20 >>> 'Energy consumption per capita'
    # --------------------------------------------------------------------------------------------------
    energy_consumption_per_capita_data = energy_data.get(
        "Energy consumption per capita", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'energy_consumption_per_capita':
        return parse_energy_consumption_per_capita(
            energy_consumption_per_capita_data
        )

    # 21
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 21 >>> 'Natural gas'
    # --------------------------------------------------------------------------------------------------
    natural_gas_data = energy_data.get("Natural gas", {})

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'natural_gas':
        return parse_natural_gas(
            natural_gas_data
        )

    # 22
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 22 >>> 'Natural gas - consumption'
    # --------------------------------------------------------------------------------------------------
    natural_gas_consumption_data = energy_data.get(
        "Natural gas - consumption", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'natural_gas_consumption':
        return parse_natural_gas_consumption(
            natural_gas_consumption_data
        )

    # 23
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 23 >>> 'Natural gas - exports'
    # --------------------------------------------------------------------------------------------------
    natural_gas_exports_data = energy_data.get("Natural gas - exports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'natural_gas_exports':
        return parse_natural_gas_exports(
            natural_gas_exports_data
        )

    # 24
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 24 >>> 'Natural gas - imports'
    # --------------------------------------------------------------------------------------------------
    natural_gas_imports_data = energy_data.get("Natural gas - imports", {})

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'natural_gas_imports':
        return parse_natural_gas_imports(
            natural_gas_imports_data
        )

    # 25
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 25 >>> 'Natural gas - production'
    # --------------------------------------------------------------------------------------------------
    natural_gas_production_data = energy_data.get(
        "Natural gas - production", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'natural_gas_production':
        return parse_natural_gas_production(
            natural_gas_production_data
        )

    # 26
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 26 >>> 'Natural gas - proved reserves'
    # --------------------------------------------------------------------------------------------------
    natural_gas_proved_reserves_data = energy_data.get(
        "Natural gas - proved reserves", {})

    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'natural_gas_proved_reserves':
        return parse_natural_gas_proved_reserves(
            natural_gas_proved_reserves_data
        )

    # 27
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 27 >>> 'Nuclear energy'
    # --------------------------------------------------------------------------------------------------
    nuclear_energy_data = energy_data.get("Nuclear energy", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'nuclear_energy':
        return parse_nuclear_energy(
            nuclear_energy_data
        )

    # 28
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 28 >>> 'Petroleum'
    # --------------------------------------------------------------------------------------------------
    petroleum_data = energy_data.get("Petroleum", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'petroleum':
        return parse_petroleum(
            petroleum_data
        )

    # 29
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 29 >>> 'Refined petroleum products - consumption'
    # --------------------------------------------------------------------------------------------------
    refined_petroleum_consumption_data = energy_data.get(
        "Refined petroleum products - consumption", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'refined_petroleum_consumption':
        return parse_refined_petroleum_consumption(
            refined_petroleum_consumption_data
        )

    # 30
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 30 >>> 'Refined petroleum products - exports'
    # --------------------------------------------------------------------------------------------------
    refined_petroleum_exports_data = energy_data.get(
        "Refined petroleum products - exports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'refined_petroleum_exports':
        return parse_refined_petroleum_exports(
            refined_petroleum_exports_data
        )

    # 31
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 31 >>> 'Refined petroleum products - imports'
    # --------------------------------------------------------------------------------------------------
    refined_petroleum_imports_data = energy_data.get(
        "Refined petroleum products - imports", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'refined_petroleum_imports':
        return parse_refined_petroleum_imports(
            refined_petroleum_imports_data
        )

    # 32
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 32 >>> 'Refined petroleum products - production'
    # --------------------------------------------------------------------------------------------------
    refined_petroleum_production_data = energy_data.get(
        "Refined petroleum products - production", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'refined_petroleum_production':
        return parse_refined_petroleum_production(
            refined_petroleum_production_data
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    # ---------------------------------------------------------------------------------------------------------------------------------
    info = 'pass'
    # ---------------------------------------------------------------------------------------------------------------------------------
    country = "USA"
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = f'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia/_raw_data'
    if country == "USA":
        region_folder = f'north-america'
        cia_code = 'us'
    elif country == "FRA":
        region_folder = f'europe'
        cia_code = 'fr'
    elif country == "WLD":
        region_folder = f'world'
        cia_code = 'xx'
    file_path = os.path.join(json_folder, region_folder, f'{cia_code}.json')
    # --------------------------------------------------------------------------------------------------
    with open(file_path, 'r', encoding='utf-8') as country_file:
        data = json.load(country_file)
    # --------------------------------------------------------------------------------------------------
    iso3Code = country
    # --------------------------------------------------------------------------------------------------
    from pprint import pprint
    pprint(
        get_energy(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
