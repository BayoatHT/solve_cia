######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import json
import logging
# ---------------------------------------------------------------------------------------------------------------------
from proj_004_cia.c_00_transform_utils.extract_and_parse import extract_and_parse
# ---------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# NOTE: "Agricultural products"
from proj_004_cia.c_06_economy.helper.utils.parse_agricultural_products import parse_agricultural_products
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Agriculture - products"
from proj_004_cia.c_06_economy.helper.utils.parse_argicultural_products_2 import parse_argicultural_products_2
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Average household expenditures"
from proj_004_cia.c_06_economy.helper.utils.parse_average_household_exp import parse_average_household_exp
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Budget"
from proj_004_cia.c_06_economy.helper.utils.parse_budget import parse_budget
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Budget surplus (+) or deficit (-)"
from proj_004_cia.c_06_economy.helper.utils.parse_budget_surplus_deficit import parse_budget_surplus_deficit
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Credit ratings"
from proj_004_cia.c_06_economy.helper.utils.parse_credit_ratings import parse_credit_ratings
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Current account balance"
from proj_004_cia.c_06_economy.helper.utils.parse_current_account_balance import parse_current_account_balance
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Debt - external"
from proj_004_cia.c_06_economy.helper.utils.parse_debt_external import parse_debt_external
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Ease of Doing Business Index scores"
from proj_004_cia.c_06_economy.helper.utils.parse_ease_of_business import parse_ease_of_business
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Economic overview"
from proj_004_cia.c_06_economy.helper.utils.parse_economic_overview import parse_economic_overview
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Exchange rates"
from proj_004_cia.c_06_economy.helper.utils.parse_exchange_rates import parse_exchange_rates
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Exports"
from proj_004_cia.c_06_economy.helper.utils.parse_exports import parse_exports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Exports - commodities"
from proj_004_cia.c_06_economy.helper.utils.parse_exports_commodities import parse_exports_commodities
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Exports - partners"
from proj_004_cia.c_06_economy.helper.utils.parse_exports_partners import parse_exports_partners
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Fiscal year"
from proj_004_cia.c_06_economy.helper.utils.parse_fiscal_year import parse_fiscal_year
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "GDP (official exchange rate)"
from proj_004_cia.c_06_economy.helper.utils.parse_gdp_official_exchange import parse_gdp_official_exchange
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "GDP (purchasing power parity) - real"
from proj_004_cia.c_06_economy.helper.utils.parse_gdp_ppp_real import parse_gdp_ppp_real
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "GDP - composition, by end use"
from proj_004_cia.c_06_economy.helper.utils.parse_gdp_composition_by_end_use import parse_gdp_composition_by_end_use
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "GDP - composition, by sector of origin"
from proj_004_cia.c_06_economy.helper.utils.parse_gdp_composition_sector_of_origin import parse_gdp_composition_sector_of_origin
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "GDP - per capita (PPP)"
from proj_004_cia.c_06_economy.helper.utils.parse_gdp_per_capita_ppp import parse_gdp_per_capita_ppp
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "GDP real growth rate"
from proj_004_cia.c_06_economy.helper.utils.parse_gdp_real_growth_rate import parse_gdp_real_growth_rate
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Gini Index coefficient - distribution of family income"
from proj_004_cia.c_06_economy.helper.utils.parse_gini import parse_gini
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Household income or consumption by percentage share"
from proj_004_cia.c_06_economy.helper.utils.parse_household_income import parse_household_income
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Imports"
from proj_004_cia.c_06_economy.helper.utils.parse_imports import parse_imports
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Imports - commodities"
from proj_004_cia.c_06_economy.helper.utils.parse_imports_commodities import parse_imports_commodities
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Imports - partners"
from proj_004_cia.c_06_economy.helper.utils.parse_imports_partners import parse_imports_partners
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Industrial production growth rate"
from proj_004_cia.c_06_economy.helper.utils.parse_industrial_production import parse_industrial_production
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Industries"
from proj_004_cia.c_06_economy.helper.utils.parse_industries import parse_industries
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Inflation rate (consumer prices)"
from proj_004_cia.c_06_economy.helper.utils.parse_inflation_rate import parse_inflation_rate
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Labor force"
from proj_004_cia.c_06_economy.helper.utils.parse_labor_force import parse_labor_force
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Labor force - by occupation"
from proj_004_cia.c_06_economy.helper.utils.parse_labor_force_by_occupation import parse_labor_force_by_occupation
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Population below poverty line"
from proj_004_cia.c_06_economy.helper.utils.parse_population_below_poverty import parse_population_below_poverty
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Public debt"
from proj_004_cia.c_06_economy.helper.utils.parse_public_debt import parse_public_debt
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Real GDP (purchasing power parity)"
from proj_004_cia.c_06_economy.helper.utils.parse_real_gdp_ppp import parse_real_gdp_ppp
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Real GDP growth rate"
from proj_004_cia.c_06_economy.helper.utils.parse_real_gdp_growth_rate import parse_real_gdp_growth_rate
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Real GDP per capita"
from proj_004_cia.c_06_economy.helper.utils.parse_real_gdp_per_capita import parse_real_gdp_per_capita
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Remittances"
from proj_004_cia.c_06_economy.helper.utils.parse_remittances import parse_remittances
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Reserves of foreign exchange and gold"
from proj_004_cia.c_06_economy.helper.utils.parse_reserves_of_foreign_exchange_and_gold import parse_reserves_of_foreign_exchange_and_gold
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Taxes and other revenues"
from proj_004_cia.c_06_economy.helper.utils.parse_taxes_and_other_revenues import parse_taxes_and_other_revenues
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Unemployment rate"
from proj_004_cia.c_06_economy.helper.utils.parse_unemployment_rate import parse_unemployment_rate
# --------------------------------------------------------------------------------------------------
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# NOTE: "Youth unemployment rate (ages 15-24)"
from proj_004_cia.c_06_economy.helper.utils.parse_youth_unemployment_rate import parse_youth_unemployment_rate
# --------------------------------------------------------------------------------------------------


# //////////////////////////////////////////////////////////////////////////////////////////////////


from proj_004_cia.c_06_economy.helper.utils.parse_economy_world import parse_economy_world


def get_economy(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: ECONOMY DATA
    # --------------------------------------------------------------------------------------------------
    eco_data = data.get("Economy", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # WORLD-SPECIFIC: Return comprehensive World economy data
    if info == 'world_economy' and iso3Code == 'WLD':
        return parse_economy_world(eco_data, iso3Code)

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'Agricultural products'
    # --------------------------------------------------------------------------------------------------
    agricultural_products_data = eco_data.get("Agricultural products", {})
    if info == 'agricultural_products':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Agricultural products",
            parser_function=parse_agricultural_products,
            iso3Code=iso3Code,
            parser_name="parse_agricultural_products"
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'Agriculture - products'
    # --------------------------------------------------------------------------------------------------
    agriculture_products_data = eco_data.get("Agriculture - products", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'argicultural_products_2':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Agriculture - products",
            parser_function=parse_argicultural_products_2,
            iso3Code=iso3Code,
            parser_name="parse_argicultural_products_2"
        )

    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'Average household expenditures'
    # --------------------------------------------------------------------------------------------------
    avg_household_expenditures_data = eco_data.get(
        "Average household expenditures", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'average_household_exp':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Average household expenditures",
            parser_function=parse_average_household_exp,
            iso3Code=iso3Code,
            parser_name="parse_average_household_exp"
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'Budget'
    # --------------------------------------------------------------------------------------------------
    budget_data = eco_data.get("", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'budget':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Budget",
            parser_function=parse_budget,
            iso3Code=iso3Code,
            parser_name="parse_budget"
        )

    # 5
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'Budget surplus (+) or deficit (-)'
    # --------------------------------------------------------------------------------------------------
    budget_surplus_deficit_data = eco_data.get(
        "Budget surplus (+) or deficit (-)", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'budget_surplus_deficit':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Budget surplus (+) or deficit (-)",
            parser_function=parse_budget_surplus_deficit,
            iso3Code=iso3Code,
            parser_name="parse_budget_surplus_deficit"
        )

    # 6
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'Credit ratings'
    # --------------------------------------------------------------------------------------------------
    credit_ratings_data = eco_data.get("Credit ratings", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'credit_ratings':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Credit rating",
            parser_function=parse_credit_ratings,
            iso3Code=iso3Code,
            parser_name="parse_credit_ratings"
        )
    # 7
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7 >>> 'Current account balance'
    # --------------------------------------------------------------------------------------------------
    current_account_balance_data = eco_data.get("Current account balance", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'current_account_balance':
        return parse_current_account_balance(iso3Code)

    # 8
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 8 >>> 'Debt - external'
    # --------------------------------------------------------------------------------------------------
    debt_external_data = eco_data.get("Debt - external", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'debt_external':
        return parse_debt_external(iso3Code)

    # 9
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 9 >>> 'Ease of Doing Business Index scores'
    # --------------------------------------------------------------------------------------------------
    ease_business_index_data = eco_data.get(
        "Ease of Doing Business Index scores", {})
    # --------------------------------------------------------------------------------------------------
    # NA
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_ease_of_business(
            ease_business_index_data
        )    
    """

    # 10
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 10 >>> 'Economic overview'
    # --------------------------------------------------------------------------------------------------
    economic_overview_data = eco_data.get("Economic overview", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'economic_overview':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Economic overview",
            parser_function=parse_economic_overview,
            iso3Code=iso3Code,
            parser_name="parse_economic_overview"
        )

    # 11
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 11 >>> 'Exchange rates'
    # --------------------------------------------------------------------------------------------------
    exchange_rates_data = eco_data.get("Exchange rates", {})
    # --------------------------------------------------------------------------------------------------
    # NA
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_echange_rates(
            pass_data
        )    
    """

    # 12
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 12 >>> 'Exports'
    # --------------------------------------------------------------------------------------------------
    exports_data = eco_data.get("Exports", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'exports':
        return parse_exports(iso3Code)

    # 13
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'Exports - commodities'
    # --------------------------------------------------------------------------------------------------
    exports_commodities_data = eco_data.get("Exports - commodities", {})
    # --------------------------------------------------------------------------------------------------

    if info == 'exports_commodities':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Exports - commodities",
            parser_function=parse_exports_commodities,
            iso3Code=iso3Code,
            parser_name="parse_exports_commodities"
        )
    # 14
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 14 >>> 'Exports - partners'
    # --------------------------------------------------------------------------------------------------
    exports_partners_data = eco_data.get("", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'exports_partners':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Exports - partners",
            parser_function=parse_exports_partners,
            iso3Code=iso3Code,
            parser_name="parse_exports_partners"
        )

    # 15
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 15 >>> 'Fiscal year'
    # --------------------------------------------------------------------------------------------------
    fiscal_year_data = eco_data.get("Fiscal year", {})
    # --------------------------------------------------------------------------------------------------
    """
    if info == 'pass':
        return parse_fiscal_year(
            pass_data
        )
    """

    # 16
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 16 >>> 'GDP (official exchange rate)'
    # --------------------------------------------------------------------------------------------------
    gdp_official_exchange_rate_data = eco_data.get(
        "GDP (official exchange rate)", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_gdp_official_exchange(
            pass_data
        )    
    """

    # 17
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 17 >>> 'GDP (purchasing power parity) - real'
    # --------------------------------------------------------------------------------------------------
    gdp_ppp_real_data = eco_data.get(
        "GDP (purchasing power parity) - real", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_gdp_ppp_real(
            pass_data
        )
    """

    # 18
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    gdp_composition_end_use_data = eco_data.get(
        "GDP - composition, by end use", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'gdp_composition_by_end_use':
        return extract_and_parse(
            main_data=eco_data,
            key_path="GDP - composition, by end use",
            parser_function=parse_gdp_composition_by_end_use,
            iso3Code=iso3Code,
            parser_name="parse_gdp_composition_by_end_use"
        )
    # 19
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    gdp_composition_sector_origin_data = eco_data.get(
        "GDP - composition, by sector of origin", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'gdp_composition_sector_of_origin':
        return extract_and_parse(
            main_data=eco_data,
            key_path="GDP - composition, by sector of origin",
            parser_function=parse_gdp_composition_sector_of_origin,
            iso3Code=iso3Code,
            parser_name="parse_gdp_composition_sector_of_origin"
        )
    # 20
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    gdp_per_capita_ppp_data = eco_data.get("GDP - per capita (PPP)", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_gdp_per_capita_ppp(
            pass_data
        )    
    """

    # 21
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 21 >>> 'GDP real growth rate'
    # --------------------------------------------------------------------------------------------------
    gdp_real_growth_rate_data = eco_data.get("GDP real growth rate", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_gdp_real_growth_rate(
            pass_data
        )
    """

    # 22
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 22 >>> 'Gini Index coefficient - distribution of family income'
    # --------------------------------------------------------------------------------------------------
    gini_index_data = eco_data.get(
        "Gini Index coefficient - distribution of family income", {})
    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'gini':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Gini Index coefficient - distribution of family income",
            parser_function=parse_gini,
            iso3Code=iso3Code,
            parser_name="parse_gini"
        )

    # 23
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 23 >>> 'Household income or consumption by percentage share'
    # --------------------------------------------------------------------------------------------------
    household_income_distribution_data = eco_data.get(
        "Household income or consumption by percentage share", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'household_income':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Household income or consumption by percentage share",
            parser_function=parse_household_income,
            iso3Code=iso3Code,
            parser_name="parse_household_income"
        )
    # 24
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 24 >>> 'Imports'
    # --------------------------------------------------------------------------------------------------
    imports_data = eco_data.get("Imports", {})
    # --------------------------------------------------------------------------------------------------
    # GET THE REST FROM WORLD BANK
    if info == 'imports':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Imports",
            parser_function=parse_imports,
            iso3Code=iso3Code,
            parser_name="parse_imports"
        )

    # 25
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    imports_commodities_data = eco_data.get("Imports - commodities", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'imports_commodities':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Imports - commodities",
            parser_function=parse_imports_commodities,
            iso3Code=iso3Code,
            parser_name="parse_imports_commodities"
        )
    # 26
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    imports_partners_data = eco_data.get("Imports - partners", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'imports_partners':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Imports - partners",
            parser_function=parse_imports_partners,
            iso3Code=iso3Code,
            parser_name="parse_imports_partners"
        )

    # 27
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    industrial_production_growth_rate_data = eco_data.get(
        "Industrial production growth rate", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'industrial_production':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Industrial production growth rate",
            parser_function=parse_industrial_production,
            iso3Code=iso3Code,
            parser_name="parse_industrial_production"
        )

    # 28
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    industries_data = eco_data.get("Industries", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'industries':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Industries",
            parser_function=parse_industries,
            iso3Code=iso3Code,
            parser_name="parse_industries"
        )

    # 29
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 29 >>> 'Inflation rate (consumer prices)'
    # --------------------------------------------------------------------------------------------------
    inflation_rate_consumer_prices_data = eco_data.get(
        "Inflation rate (consumer prices)", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'inflation_rate':
        return parse_inflation_rate(iso3Code)

    # 30
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    labor_force_data = eco_data.get("Labor force", {})
    # --------------------------------------------------------------------------------------------------
    """
    if info == 'pass':
        return parse_labor_force(
            pass_data
        )
    """

    # 31
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    labor_force_by_occupation_data = eco_data.get(
        "Labor force - by occupation", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'labor_force_by_occupation':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Labor force - by occupation",
            parser_function=parse_labor_force_by_occupation,
            iso3Code=iso3Code,
            parser_name="parse_labor_force_by_occupation"
        )

    # 32
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    population_below_poverty_line_data = eco_data.get(
        "Population below poverty line", {})
    # --------------------------------------------------------------------------------------------------
    """
    if info == 'pass':
        return parse_population_below_poverty(
            pass_data
        )
    """

    # 33
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 33 >>> 'Public debt'
    # --------------------------------------------------------------------------------------------------
    public_debt_data = eco_data.get("Public debt", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'public_debt':
        return parse_public_debt(iso3Code)

    # 34
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    real_gdp_ppp_data = eco_data.get("Real GDP (purchasing power parity)", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_real_gdp_ppp(
            real_gdp_ppp_data
        )    
    """

    # 35
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    real_gdp_growth_rate_data = eco_data.get("Real GDP growth rate", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # --------------------------------------------------------------------------------------------------
    # pass
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_real_gdp_growth_rate(
            real_gdp_growth_rate_data
        )    
    """

    # 36
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    gdp_capita_data = eco_data.get("Real GDP per capita", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    """
    if info == 'pass':
        return parse_real_gdp_per_capita(
            gdp_capita_data
        )
    """

    # 37
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    remittances_data = eco_data.get("Remittances", {})
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'remittances':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Remittances",
            parser_function=parse_remittances,
            iso3Code=iso3Code,
            parser_name="parse_remittances"
        )
    # 38
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # --------------------------------------------------------------------------------------------------
    reserves_foreign_exchange_gold_data = eco_data.get(
        "Reserves of foreign exchange and gold", {})
    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'reserves_of_foreign_exchange_and_gold':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Reserves of foreign exchange and gold",
            parser_function=parse_reserves_of_foreign_exchange_and_gold,
            iso3Code=iso3Code,
            parser_name="parse_reserves_of_foreign_exchange_and_gold"
        )

    # 39
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    taxes_revenues_data = eco_data.get("Taxes and other revenues", {})
    # --------------------------------------------------------------------------------------------------
    """
    if info == 'pass':
        return parse_taxes_and_other_revenues(
            pass_data
        )
    """

    # 40
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 40 >>> 'Unemployment rate'
    # --------------------------------------------------------------------------------------------------
    unemployment_rate_data = eco_data.get("Unemployment rate", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'unemployment_rate':
        return parse_unemployment_rate(iso3Code)

    # 41
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 41 >>> 'Youth unemployment rate (ages 15-24)'
    # --------------------------------------------------------------------------------------------------
    youth_unemployment_rate_data = eco_data.get(
        "Youth unemployment rate (ages 15-24)", {})
    # --------------------------------------------------------------------------------------------------
    if info == 'youth_unemployment_rate':
        return extract_and_parse(
            main_data=eco_data,
            key_path="Youth unemployment rate (ages 15-24)",
            parser_function=parse_youth_unemployment_rate,
            iso3Code=iso3Code,
            parser_name="parse_youth_unemployment_rate"
        )


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
    pprint(get_economy(data=data, info=info, iso3Code=iso3Code))
