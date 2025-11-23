######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import json
import logging
# -----------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
# "Age structure" - ['structure_age_0_14', 'structure_age_15_24', 'structure_age_15_64', 'structure_age_25_54', 'structure_age_55_64', 'structure_age_65_over']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_age_structure import parse_age_structure
# "Alcohol consumption per capita" - ['alc_consumed_beer', 'alc_consumed_other', 'alc_consumed_spirits', 'alc_consumed_total', 'alc_consumed_wine']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_alcohol import parse_alcohol
# "Birth rate" - ['birth_rate_note', 'birth_rate']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_birth_rate import parse_birth_rate
# "Child marriage" - ['men_married_18', 'women_married_15', 'women_married_18']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_child_marriage import parse_child_marriage
# "Children under the age of 5 years underweight" - ['child_underweight_note', 'child_underweight']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_child_under_5_under_weight import parse_child_under_5_under_weight
# "Contraceptive prevalence rate" - ['contraceptive_note', 'contraceptive']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_contraceptive_rate import parse_contraceptive_rate
# "Current health expenditure" - ['health_expenditure_note', 'health_expenditure']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_health_expenditure import parse_health_expenditure
# "Currently married women (ages 15-49)" - ['married_women_15_49_note', 'married_womwn_15_49']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_women_married_15_49 import parse_women_married_15_49
# "Death rate" - ['death_rate_note', 'death_rate']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_death_rate import parse_death_rate
# "Demographic profile" - ['demo_profile']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_demographic_profile import parse_demographic_profile
# "Dependency ratios" - ['elderly_dependency_ratio', 'dependency_note', 'potential_support_ratio',
# 'total_dependency_ratio', 'youth_dependency_ratio']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_dependency_ratios import parse_dependency_ratios
# "Drinking water source" - ['drink_water_improved_rural', 'drink_water_improved_total', 'drink_water_improved_urban',
# 'drink_water_note', 'drink_water_unimproved_rural', 'drink_water_unimproved_total',
# 'drink_water_unimproved_urban']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_drinking_water_source import parse_drinking_water_source
# "Education expenditures" - ['education_expenditure_note', 'education_expenditure']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_education_expenditure import parse_education_expenditure
# "Ethnic groups" - ['ethinic_groups','ethnic_groups_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_ethnic_groups import parse_ethnic_groups
# "Gross reproduction rate" - ['reproduction_rate']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_reproduction_rate import parse_reproduction_rate
# "HIV/AIDS - adult prevalence rate" - ['hiv_adult_rate']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_hiv_rate import parse_hiv_rate
# "HIV/AIDS - deaths" - ['hiv_deaths']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_hiv_deaths import parse_hiv_deaths
# "HIV/AIDS - people living with HIV/AIDS" - ['hiv_living']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_hiv_living_with import parse_hiv_living_with
# "Hospital bed density" - ['hospital_density_note', 'hospital_density']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_hospital_bed_density import parse_hospital_bed_density
# "Infant mortality rate" - ['infant_mortality_female','infant_mortality_male','infant_mortality_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_infant_mortality import parse_infant_mortality
# "Languages" - ['languages', 'major_languages', 'languages_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_languages import parse_languages
# "Life expectancy at birth" - ['life_expect_female', 'life_expect_male', 'life_expect_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_life_expectancy_at_birth import parse_life_expectancy_at_birth
# "Literacy" - ['literacy_def', 'literacy_female', 'literacy_male', 'literacy_note', 'literacy_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_literacy import parse_literacy
# "Major infectious diseases" - ['infect_dust_soil', 'infect_animal', 'infect_risk', 'infect_food_water', 'infect_note',
# 'infect_respiratory', 'infect_soil', 'infect_vector', 'infect_water']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_infectious_diseases import parse_infectious_diseases
# "Major urban areas - population" - ['urb_pop_note', 'urb_pop']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_major_urban_areas import parse_major_urban_areas
# "Maternal mortality ratio" - ['maternal_note', 'maternal']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_maternal_mortality import parse_maternal_mortality
# "Median age" - ['median_age_female', 'median_age_male', 'median_age_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_median_age import parse_median_age
# "Mother's mean age at first birth" - ['first_birth_note', 'first_birth']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_mothers_age_at_first_birth import parse_mothers_age_at_first_birth
# "Nationality" - ['nationality_adjective', 'nationality_note', 'nationality_noun']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_nationality import parse_nationality
# "Net migration rate" - ['migration_rate']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_net_migration_rate import parse_net_migration_rate
# "Obesity - adult prevalence rate" - ['obesity_note', 'obesity']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_obesity import parse_obesity
# "People - note" - ['people_note']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_people_note import parse_people_note
# "Physician density" - ['doctors_density_note', 'doctors_density']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_physician_density import parse_physician_density
# "Population" - ['population_female', 'population_male', 'population_note', 'population_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_population import parse_population
# "Population distribution" - ['pop_distro_note', 'pop_distro']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_population_distribution import parse_population_distribution
# "Population growth rate" - ['pop_growth_note', 'pop_growth']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_population_growth import parse_population_growth
# "Religions" - ['religions_note', 'religions']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_religions import parse_religions
# "Sanitation facility access" - ['sanitation_improved_rural', 'sanitation_improved_total', 'sanitation_improved_urban',
# 'sanitation_note', 'sanitation_unimproved_rural', 'sanitation_unimproved_total',
# 'sanitation_unimproved_urban']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_sanitation_access import parse_sanitation_access
# "School life expectancy (primary to tertiary education)" - ['school_life_female','school_life_male','school_life_note','school_life_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_school_life_expectancy import parse_school_life_expectancy
# "Sex ratio" - ['sex_ratio_0_14', 'sex_ratio_15_24','sex_ratio_15_64','sex_ratio_25_54','sex_ratio_55_64',
# 'sex_ratio_65_over', 'sex_ratio_birth', 'sex_ratio_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_sex_ratio import parse_sex_ratio
# "Tobacco use" - ['tobacco_female','tobacco_male','tobacco_total']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_tobacco_use import parse_tobacco_use
# "Total fertility rate" - ['fertility_rate']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_fertility_rate import parse_fertility_rate
# "Urbanization" - ['urban_note', 'urban_rate', 'urban_pop']
# --------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.utils.parse_urbanization import parse_urbanization
# --------------------------------------------------------------------------------------------------
# #/////////////////////////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////////////////////////////////////////


def get_society(data=None, info=None, iso3Code=None):

    # 0
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: SOCIETY DATA
    # --------------------------------------------------------------------------------------------------
    society_data = data.get("People and Society", {})
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # 1
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 1 >>> 'Age structure'
    # --------------------------------------------------------------------------------------------------
    age_data = society_data.get("Age structure", {})
    # --------------------------------------------------------------------------------------------------
    # "0-14 years" - 'structure_age_0_14'
    # "15-24 years" - 'structure_age_15_24'
    # "15-64 years" - 'structure_age_15_64'
    # "25-54 years" - 'structure_age_25_54'
    # "55-64 years" - 'structure_age_55_64'
    # "65 years and over" - 'structure_age_65_over'
    # --------------------------------------------------------------------------------------------------
    # ['structure_age_0_14', 'structure_age_15_24', 'structure_age_15_64', 'structure_age_25_54', 'structure_age_55_64', 'structure_age_65_over']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'age_structure':
        return parse_age_structure(
            age_data
        )

    # 2
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 2 >>> 'Alcohol consumption per capita'
    # --------------------------------------------------------------------------------------------------
    alcohol_data = society_data.get("Alcohol consumption per capita", {})
    # --------------------------------------------------------------------------------------------------
    # "beer" - alc_consumed_beer
    # "other alcohols" - alc_consumed_other
    # "spirits" - alc_consumed_spirits
    # "total" - alc_consumed_total
    # "wine" - alc_consumed_wine
    # --------------------------------------------------------------------------------------------------
    # ['alc_consumed_beer', 'alc_consumed_other', 'alc_consumed_spirits', 'alc_consumed_total', 'alc_consumed_wine']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'alcohol':
        return parse_alcohol(
            alcohol_data
        )

    # 3
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 3 >>> 'Birth rate'
    # --------------------------------------------------------------------------------------------------
    birth_data = society_data.get("Birth rate", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - birth_rate_note
    # "text", - birth_rate
    # --------------------------------------------------------------------------------------------------
    # ['birth_rate_note', 'birth_rate']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'birth_rate':
        return parse_birth_rate(
            birth_data
        )

    # 4
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 4 >>> 'Child marriage'
    # --------------------------------------------------------------------------------------------------
    child_marriage_data = society_data.get("Child marriage", {})
    # --------------------------------------------------------------------------------------------------
    # "men married by age 18" - men_marrried_18
    # "note"
    # "women married by age 15" - women_married_15
    # "women married by age 18" - women_married_18
    # --------------------------------------------------------------------------------------------------
    # ['men_married_18', 'women_married_15', 'women_married_18']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'child_marriage':
        return parse_child_marriage(
            child_marriage_data
        )

    # 5
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 5 >>> 'Children under the age of 5 years underweight'
    # --------------------------------------------------------------------------------------------------
    child_underweight_data = society_data.get(
        "Children under the age of 5 years underweight", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - child_underweight_note
    # "text", - child_underweight
    # --------------------------------------------------------------------------------------------------
    # ['child_underweight_note', 'child_underweight']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'child_under_5_under_weight':
        return parse_child_under_5_under_weight(
            child_underweight_data
        )

    # 6
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 6 >>> 'Contraceptive prevalence rate'
    # --------------------------------------------------------------------------------------------------
    contraceptive_data = society_data.get("Contraceptive prevalence rate", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - contraceptive_note
    # "text", - contraceptive
    # --------------------------------------------------------------------------------------------------
    # ['contraceptive_note', 'contraceptive']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'contraceptive_rate':
        return parse_contraceptive_rate(
            contraceptive_data
        )

    # 7
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 7 >>> 'Current health expenditure'
    # --------------------------------------------------------------------------------------------------
    health_expenditure_data = society_data.get(
        "Current health expenditure", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - health_expenditure_note
    # "text", - health_expenditure
    # --------------------------------------------------------------------------------------------------
    # ['health_expenditure_note', 'health_expenditure']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'health_expenditure':
        return parse_contraceptive_rate(
            health_expenditure_data
        )
    # 8
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 8 >>> 'Currently married women (ages 15-49)'
    # --------------------------------------------------------------------------------------------------
    married_women_data = society_data.get(
        "Currently married women (ages 15-49)", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - married_women_15_49_note
    # "text", - married_woman_15_49
    # --------------------------------------------------------------------------------------------------
    # ['married_women_15_49_note', 'married_woman_15_49']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'women_married_15_49':
        return parse_women_married_15_49(
            married_women_data
        )

    # 9
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 9 >>> 'Death rate'
    # --------------------------------------------------------------------------------------------------
    death_rate_data = society_data.get(
        "Death rate", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'death_rate_note'
    # "text" - 'death_rate'
    # --------------------------------------------------------------------------------------------------
    # ['death_rate_note', 'death_rate']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'death_rate':
        return parse_death_rate(
            death_rate_data
        )
    # 10
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 10 >>> 'Demographic profile'
    # --------------------------------------------------------------------------------------------------
    demo_data = society_data.get(
        "Demographic profile", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'demo_profile'
    # --------------------------------------------------------------------------------------------------
    # ['demo_profile']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'demographic_profile':
        return parse_demographic_profile(
            demo_data
        )

    # 11
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 11 >>> 'Dependency ratios'
    # --------------------------------------------------------------------------------------------------
    dependency_data = society_data.get(
        "Dependency ratios", {})
    # --------------------------------------------------------------------------------------------------
    # "elderly dependency ratio" - 'elderly_dependency_ratio'
    # "note" - 'dependency_note'
    # "potential support ratio" - 'potential_support_ratio'
    # "total dependency ratio" - 'total_dependency_ratio'
    # "youth dependency ratio" -  'youth_dependency_ratio'
    # --------------------------------------------------------------------------------------------------
    # ['elderly_dependency_ratio', 'dependency_note', 'potential_support_ratio',
    # 'total_dependency_ratio', 'youth_dependency_ratio']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'dependency_ratios':
        return parse_dependency_ratios(
            dependency_data
        )

    # 12
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 12 >>> 'Drinking water source'
    # --------------------------------------------------------------------------------------------------
    drinking_data = society_data.get(
        "Drinking water source", {})
    # --------------------------------------------------------------------------------------------------
    # "improved: rural" - 'drink_water_improved_rural'
    # "improved: total" - 'drink_water_improved_total'
    # "improved: urban" - 'drink_water_improved_urban'
    # "note" - 'drink_water_note'
    # "unimproved: rural" - 'drink_water_unimproved_rural'
    # "unimproved: total" - 'drink_water_unimproved_total'
    # "unimproved: urban" - 'drink_water_unimproved_urban'
    # --------------------------------------------------------------------------------------------------
    # ['drink_water_improved_rural', 'drink_water_improved_total', 'drink_water_improved_urban',
    # 'drink_water_note', 'drink_water_unimproved_rural', 'drink_water_unimproved_total',
    # 'drink_water_unimproved_urban']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'drinking_water_source':
        return parse_drinking_water_source(
            drinking_data
        )
    # 13
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 13 >>> 'Education expenditures'
    # --------------------------------------------------------------------------------------------------
    ed_data = society_data.get(
        "Education expenditures", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'education_expenditure_note'
    # "text" - 'education_expenditure'
    # --------------------------------------------------------------------------------------------------
    # ['education_expenditure_note', 'education_expenditure']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'education_expenditure':
        return parse_education_expenditure(
            ed_data
        )

    # 14
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 14 >>> 'Ethnic groups'
    # --------------------------------------------------------------------------------------------------
    ethnic_data = society_data.get(
        "Ethnic groups", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'ethinic_groups_note'
    # "text" - 'ethnic_groups
    # --------------------------------------------------------------------------------------------------
    # ['ethinic_groups','ethnic_groups_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'ethnic_groups':
        return parse_ethnic_groups(
            ethnic_data
        )

    # 15
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 15 >>> 'Gross reproduction rate'
    # --------------------------------------------------------------------------------------------------
    reproduction_data = society_data.get(
        "Gross reproduction rate", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'reproduction_rate'
    # --------------------------------------------------------------------------------------------------
    # ['reproduction_rate']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'reproduction_rate':
        return parse_reproduction_rate(
            reproduction_data
        )
    # 16
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 16 >>> 'HIV/AIDS - adult prevalence rate'
    # --------------------------------------------------------------------------------------------------
    hiv_adult_data = society_data.get(
        "HIV/AIDS - adult prevalence rate", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'hiv_adult_rate'
    # --------------------------------------------------------------------------------------------------
    # ['hiv_adult_rate']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'hiv_rate':
        return parse_hiv_rate(
            hiv_adult_data
        )
    # 17
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 17 >>> 'HIV/AIDS - deaths'
    # --------------------------------------------------------------------------------------------------
    hiv_deaths_data = society_data.get(
        "HIV/AIDS - deaths", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'hiv_deaths'
    # --------------------------------------------------------------------------------------------------
    # ['hiv_deaths']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'hiv_deaths':
        return parse_hiv_deaths(
            hiv_deaths_data
        )

    # 18
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 18 >>> 'HIV/AIDS - people living with HIV/AIDS'
    # --------------------------------------------------------------------------------------------------
    hiv_living_data = society_data.get(
        "HIV/AIDS - people living with HIV/AIDS", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'hiv_living'
    # --------------------------------------------------------------------------------------------------
    # ['hiv_living']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'hiv_living_with':
        return parse_hiv_living_with(
            hiv_living_data
        )

    # 19
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 19 >>> 'Hospital bed density'
    # --------------------------------------------------------------------------------------------------
    hospital_density_data = society_data.get("Hospital bed density", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - 'hospital_density_note'
    # "text", - 'hospital_density'
    # --------------------------------------------------------------------------------------------------
    # ['hospital_density_note', 'hospital_density']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'hospital_bed_density':
        return parse_hospital_bed_density(
            hospital_density_data
        )

    # 20
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 20 >>> 'Infant mortality rate'
    # --------------------------------------------------------------------------------------------------
    infant_data = society_data.get("Infant mortality rate", {})
    # --------------------------------------------------------------------------------------------------
    # "female" - 'infant_mortality_female'
    # "male", - 'infant_mortality_male'
    # "total" - 'infant_mortality_total'
    # --------------------------------------------------------------------------------------------------
    # ['infant_mortality_female','infant_mortality_male','infant_mortality_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'infant_mortality':
        return parse_infant_mortality(
            infant_data
        )

        s
    # 21
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 21 >>> 'Languages'
    # --------------------------------------------------------------------------------------------------
    languages_data = society_data.get("Languages", {})
    # --------------------------------------------------------------------------------------------------
    # "Languages" - 'languages'
    # "major-language sample(s)" - 'major_languages'
    # "note" - 'languages_note'
    # --------------------------------------------------------------------------------------------------
    # ['languages', 'major_languages', 'languages_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'languages':
        return parse_languages(
            languages_data
        )

    # 22
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 22 >>> 'Life expectancy at birth'
    # --------------------------------------------------------------------------------------------------
    life_expectancy_data = society_data.get("Life expectancy at birth", {})
    # --------------------------------------------------------------------------------------------------
    # "female" - 'life_expect_female'
    # "male" - 'life_expect_male'
    # "total population" - 'life_expect_total'
    # --------------------------------------------------------------------------------------------------
    # ['life_expect_female', 'life_expect_male', 'life_expect_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'life_expectancy_at_birth':
        return parse_life_expectancy_at_birth(
            life_expectancy_data
        )

    # 23
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 23 >>> 'Literacy'
    # --------------------------------------------------------------------------------------------------
    literacy_data = society_data.get("Literacy", {})
    # --------------------------------------------------------------------------------------------------
    # "definition" - 'literacy_def'
    # "female" - 'literacy_female'
    # "male" - 'literacy_male'
    # "note" - 'literacy_note'
    # "total population" - 'literacy_total'
    # --------------------------------------------------------------------------------------------------
    # ['literacy_def', 'literacy_female', 'literacy_male', 'literacy_note', 'literacy_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'literacy':
        return parse_literacy(
            literacy_data
        )

    # 24
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 24 >>> 'Major infectious diseases'
    # --------------------------------------------------------------------------------------------------
    infect_data = society_data.get("Major infectious diseases", {})
    # --------------------------------------------------------------------------------------------------
    # "aerosolized dust or soil contact diseases" - 'infect_dust_soil'
    # "animal contact diseases" - 'infect_animal'
    # "degree of risk" - 'infect_risk'
    # "food or waterborne diseases" - 'infect_food_water'
    # "note" - 'infect_note'
    # "respiratory diseases" - 'infect_respiratory'
    # "soil contact diseases" - 'infect_soil'
    # "vectorborne diseases" - 'infect_vector'
    # "water contact diseases" - 'infect_water'
    # --------------------------------------------------------------------------------------------------
    # ['infect_dust_soil', 'infect_animal', 'infect_risk', 'infect_food_water', 'infect_note',
    # 'infect_respiratory', 'infect_soil', 'infect_vector', 'infect_water']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'infectious_diseases':
        return parse_infectious_diseases(
            infect_data
        )

    # 25
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 25 >>> 'Major urban areas - population'
    # --------------------------------------------------------------------------------------------------
    urb_pop_data = society_data.get("Major urban areas - population", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'urb_pop_note'
    # "text" - 'urb_pop'
    # --------------------------------------------------------------------------------------------------
    # ['urb_pop_note', 'urb_pop']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'major_urban_areas':
        return parse_major_urban_areas(
            urb_pop_data
        )

    # 26
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 25 >>> 'Maternal mortality ratio'
    # --------------------------------------------------------------------------------------------------
    maternal_data = society_data.get("Maternal mortality ratio", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'maternal_note'
    # "text" - 'maternal'
    # --------------------------------------------------------------------------------------------------
    # ['maternal_note', 'maternal']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'maternal_mortality':
        return parse_maternal_mortality(
            maternal_data
        )

    # 27
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 27 >>> 'Median age'
    # --------------------------------------------------------------------------------------------------
    median_age_data = society_data.get("Median age", {})
    # --------------------------------------------------------------------------------------------------
    # "female" - 'median_age_female'
    # "male", - 'median_age_male'
    # "total", - 'median_age_total'
    # --------------------------------------------------------------------------------------------------
    # ['median_age_female', 'median_age_male', 'median_age_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'median_age':
        return parse_median_age(
            median_age_data
        )

    # 28
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 28 >>> 'Mother's mean age at first birth'
    # --------------------------------------------------------------------------------------------------
    first_birth_data = society_data.get("Mother's mean age at first birth", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'first_birth_note'
    # "text" - 'first_birth'
    # --------------------------------------------------------------------------------------------------
    # ['first_birth_note', 'first_birth']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'mothers_age_at_first_birth':
        return parse_mothers_age_at_first_birth(
            first_birth_data
        )

    # 29
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 29 >>> 'Nationality'
    # --------------------------------------------------------------------------------------------------
    nationality_data = society_data.get("Nationality", {})
    # --------------------------------------------------------------------------------------------------
    # "adjective", - 'nationality_adjective'
    # "note", - 'nationality_note'
    # "noun"  - 'nationality_noun'
    # --------------------------------------------------------------------------------------------------
    # ['nationality_adjective', 'nationality_note', 'nationality_noun']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'nationality':
        return parse_nationality(
            nationality_data
        )

    # 30
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 30 >>> 'Net migration rate'
    # --------------------------------------------------------------------------------------------------
    migration_data = society_data.get("Net migration rate", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'migration_rate'
    # --------------------------------------------------------------------------------------------------
    # ['migration_rate']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'net_migration_rate':
        return parse_net_migration_rate(
            migration_data
        )
    # 31
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 31 >>> 'Obesity - adult prevalence rate'
    # --------------------------------------------------------------------------------------------------
    obesity_data = society_data.get("Obesity - adult prevalence rate", {})
    # --------------------------------------------------------------------------------------------------
    # 'note' - 'obesity_note'
    # 'text' - 'obesity'
    # --------------------------------------------------------------------------------------------------
    # ['obesity_note', 'obesity']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'obesity':
        return parse_obesity(
            obesity_data
        )

    # 32
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 32 >>> 'Physician density'
    # --------------------------------------------------------------------------------------------------
    doctors_data = society_data.get("Physician density", {})
    # --------------------------------------------------------------------------------------------------
    # 'note' - 'doctors_density_note'
    # 'text' - 'doctors_density'
    # --------------------------------------------------------------------------------------------------
    # ['doctors_density_note', 'doctors_density']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'physician_density':
        return parse_physician_density(
            doctors_data
        )

    # 33
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 33 >>> 'Population'
    # --------------------------------------------------------------------------------------------------
    pop_data = society_data.get("Population", {})
    # --------------------------------------------------------------------------------------------------
    # "female" - 'population_female'
    # "male" - 'population_male'
    # "note" - 'population_note'
    # "total" - 'population_total'
    # --------------------------------------------------------------------------------------------------
    # ['population_female', 'population_male', 'population_note', 'population_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'population':
        return parse_population(
            pop_data
        )

    # 34
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 34 >>> 'Population distribution'
    # --------------------------------------------------------------------------------------------------
    pop_distro_data = society_data.get("Population distribution", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - 'pop_distro_note'
    # "text", - 'pop_distro'
    # --------------------------------------------------------------------------------------------------
    # ['pop_distro_note', 'pop_distro']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'population_distribution':
        return parse_population_distribution(
            pop_distro_data
        )

    # 35
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 35 >>> 'Population growth rate'
    # --------------------------------------------------------------------------------------------------
    pop_growth_data = society_data.get("Population growth rate", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'pop_growth_note'
    # "text" - 'pop_growth'
    # --------------------------------------------------------------------------------------------------
    # ['pop_growth_note', 'pop_growth']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'population_growth':
        return parse_population_growth(
            pop_growth_data
        )

    # 36
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 36 >>> 'Religions'
    # --------------------------------------------------------------------------------------------------
    religions_data = society_data.get("Religions", {})
    # --------------------------------------------------------------------------------------------------
    # "note", - 'religions_note'
    # "text", - 'religions'
    # --------------------------------------------------------------------------------------------------
    # ['religions_note', 'religions']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'religions':
        return parse_religions(
            religions_data
        )

    # 37
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 37 >>> 'Sanitation facility access'
    # --------------------------------------------------------------------------------------------------
    sanitation_data = society_data.get("Sanitation facility access", {})
    # --------------------------------------------------------------------------------------------------
    # "improved: rural" - 'sanitation_improved_rural'
    # "improved: total" - 'sanitation_improved_total'
    # "improved: urban" - 'sanitation_improved_urban'
    # "note" - 'sanitation_note'
    # "unimproved: rural" - 'sanitation_unimproved_rural'
    # "unimproved: total" - 'sanitation_unimproved_total'
    # "unimproved: urban" - 'sanitation_unimproved_urban'
    # --------------------------------------------------------------------------------------------------
    # ['sanitation_improved_rural', 'sanitation_improved_total', 'sanitation_improved_urban',
    # 'sanitation_note', 'sanitation_unimproved_rural', 'sanitation_unimproved_total',
    # 'sanitation_unimproved_urban']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'sanitation_access':
        return parse_sanitation_access(
            sanitation_data
        )

    # 38
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 38 >>> 'School life expectancy (primary to tertiary education)'
    # --------------------------------------------------------------------------------------------------
    school_life_data = society_data.get(
        "School life expectancy (primary to tertiary education)", {})
    # --------------------------------------------------------------------------------------------------
    # "female" - 'school_life_female'
    # "male" - 'school_life_male'
    # "note" - 'school_life_note'
    # "total" - 'school_life_total'
    # --------------------------------------------------------------------------------------------------
    # ['school_life_female','school_life_male','school_life_note','school_life_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'school_life_expectancy':
        return parse_school_life_expectancy(
            school_life_data
        )

    # 39
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 39 >>> 'Sex ratio'
    # --------------------------------------------------------------------------------------------------
    sex_data = society_data.get("Sex ratio", {})
    # --------------------------------------------------------------------------------------------------
    # "0-14 years" - 'sex_ratio_0_14'
    # "15-24 years" - 'sex_ratio_15_24'
    # "15-64 years" - 'sex_ratio_15_64'
    # "25-54 years" - 'sex_ratio_25_54'
    # "55-64 years" - 'sex_ratio_55_64'
    # "65 years and over" - 'sex_ratio_65_over'
    # "at birth" - 'sex_ratio_birth'
    # "total population" - 'sex_ratio_total'
    # --------------------------------------------------------------------------------------------------
    # ['sex_ratio_0_14', 'sex_ratio_15_24','sex_ratio_15_64','sex_ratio_25_54','sex_ratio_55_64',
    # 'sex_ratio_65_over', 'sex_ratio_birth', 'sex_ratio_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'sex_ratio':
        return parse_sex_ratio(
            sex_data
        )

    # 40
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 40 >>> 'Tobacco use'
    # --------------------------------------------------------------------------------------------------
    tobacco_data = society_data.get("Tobacco use", {})
    # --------------------------------------------------------------------------------------------------
    # "female" - 'tobacco_female'
    # "male" - 'tobacco_male'
    # "total" - 'tobacco_total'
    # --------------------------------------------------------------------------------------------------
    # ['tobacco_female','tobacco_male','tobacco_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'tobacco_use':
        return parse_tobacco_use(
            tobacco_data
        )

    # 41
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 41 >>> 'Total fertility rate'
    # --------------------------------------------------------------------------------------------------
    fertility_data = society_data.get("Total fertility rate", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'fertility_rate'
    # --------------------------------------------------------------------------------------------------
    # ['fertility_rate']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'fertility_rate':
        return parse_fertility_rate(
            fertility_data
        )

    # 42
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 42 >>> 'People - note'
    # --------------------------------------------------------------------------------------------------
    people_note_data = society_data.get("People - note", {})
    # --------------------------------------------------------------------------------------------------
    # text - 'people_note'
    # --------------------------------------------------------------------------------------------------
    # ['people_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'people_note':
        return parse_people_note(
            people_note_data
        )

    # 43
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # NOTE: 43 >>> 'Urbanization'
    # --------------------------------------------------------------------------------------------------
    urban_data = society_data.get("Urbanization", {})
    # --------------------------------------------------------------------------------------------------
    # "note" - 'urban_note'
    # "rate of urbanization" - 'urban_rate'
    # "urban population" - 'urban_pop'
    # --------------------------------------------------------------------------------------------------
    # ['urban_note', 'urban_rate', 'urban_pop']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    if info == 'urbanization':
        return parse_urbanization(
            urban_data
        )


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    # --------------------------------------------------------------------------------------------------
    info = 'pass'
    # ---------------------------
    country = "USA"
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = f'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia/_raw_data'
    if country == "USA":
        region_folder = f'north-america'
        cia_code = 'us'
    if country == "FRA":
        region_folder = f'europe'
        cia_code = 'fr'
    if country == "WLD":
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
        get_society(
            data=data,
            info=info,
            iso3Code=iso3Code
        )
    )
