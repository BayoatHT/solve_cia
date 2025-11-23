'''
#   PURPOSE OF THIS FILE
    >>> RETURN A DICTIONARY OF GEOGRAPHY INFORMATION FROM THE CIA WORLD FACTBOOK
'''


#######################################################################################################################

######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import json
import os
# get_society  ------------------------------------------------------------------------------------------------------
from proj_004_cia.c_03_society.helper.get_society import get_society

######################################################################################################################
#   CORE FUNCTION
# ---------------------------------------------------------------------------------------------------------------------


def return_society_data(
        data: dict,
        iso3Code: str
):
    # Initialize the dictionary to hold geography data
    cia_pack = {}

    # Conditional inclusion based on iso3Code
    if iso3Code != 'WLD':
        # Note: 'age_structure'
        cia_pack['age_structure'] = get_society(
            data=data, info='age_structure', iso3Code=iso3Code)
        # Note: 'alcohol'
        cia_pack['alcohol'] = get_society(
            data=data, info='alcohol', iso3Code=iso3Code)
        # Note: 'birth_rate'
        cia_pack['birth_rate'] = get_society(
            data=data, info='birth_rate', iso3Code=iso3Code)
        # Note: 'child_marriage'
        cia_pack['child_marriage'] = get_society(
            data=data, info='child_marriage', iso3Code=iso3Code)
        # Note: 'child_under_5_under_weight'
        cia_pack['child_under_5_under_weight'] = get_society(
            data=data, info='child_under_5_under_weight', iso3Code=iso3Code)
        # Note: 'contraceptive_rate'
        cia_pack['contraceptive_rate'] = get_society(
            data=data, info='contraceptive_rate', iso3Code=iso3Code)
        # Note: 'health_expenditure'
        cia_pack['health_expenditure'] = get_society(
            data=data, info='health_expenditure', iso3Code=iso3Code)
        # Note: 'women_married_15_49'
        cia_pack['women_married_15_49'] = get_society(
            data=data, info='women_married_15_49', iso3Code=iso3Code)
        # Note: 'death_rate'
        cia_pack['death_rate'] = get_society(
            data=data, info='death_rate', iso3Code=iso3Code)
        # Note: 'demographic_profile'
        cia_pack['demographic_profile'] = get_society(
            data=data, info='demographic_profile', iso3Code=iso3Code)
        # Note: 'dependency_ratios'
        cia_pack['dependency_ratios'] = get_society(
            data=data, info='dependency_ratios', iso3Code=iso3Code)
        # Note: 'drinking_water_source'
        cia_pack['drinking_water_source'] = get_society(
            data=data, info='drinking_water_source', iso3Code=iso3Code)
        # Note: 'education_expenditure'
        cia_pack['education_expenditure'] = get_society(
            data=data, info='education_expenditure', iso3Code=iso3Code)
        # Note: 'ethnic_groups'
        cia_pack['ethnic_groups'] = get_society(
            data=data, info='ethnic_groups', iso3Code=iso3Code)
        # Note: 'reproduction_rate'
        cia_pack['reproduction_rate'] = get_society(
            data=data, info='reproduction_rate', iso3Code=iso3Code)
        # Note: 'hiv_rate'
        cia_pack['hiv_rate'] = get_society(
            data=data, info='hiv_rate', iso3Code=iso3Code)
        # Note: 'hiv_deaths'
        cia_pack['hiv_deaths'] = get_society(
            data=data, info='hiv_deaths', iso3Code=iso3Code)
        # Note: 'hiv_living_with'
        cia_pack['hiv_living_with'] = get_society(
            data=data, info='hiv_living_with', iso3Code=iso3Code)
        # Note: 'hospital_bed_density'
        cia_pack['hospital_bed_density'] = get_society(
            data=data, info='hospital_bed_density', iso3Code=iso3Code)
        # Note: 'infant_mortality'
        cia_pack['infant_mortality'] = get_society(
            data=data, info='infant_mortality', iso3Code=iso3Code)
        # Note: 'languages'
        cia_pack['languages'] = get_society(
            data=data, info='languages', iso3Code=iso3Code)
        # Note: 'life_expectancy_at_birth'
        cia_pack['life_expectancy_at_birth'] = get_society(
            data=data, info='life_expectancy_at_birth', iso3Code=iso3Code)
        # Note: 'literacy'
        cia_pack['literacy'] = get_society(
            data=data, info='literacy', iso3Code=iso3Code)
        # Note: 'infectious_diseases'
        cia_pack['infectious_diseases'] = get_society(
            data=data, info='infectious_diseases', iso3Code=iso3Code)
        # Note: 'major_urban_areas'
        cia_pack['major_urban_areas'] = get_society(
            data=data, info='major_urban_areas', iso3Code=iso3Code)
        # Note: 'maternal_mortality'
        cia_pack['maternal_mortality'] = get_society(
            data=data, info='maternal_mortality', iso3Code=iso3Code)
        # Note: 'median_age'
        cia_pack['median_age'] = get_society(
            data=data, info='median_age', iso3Code=iso3Code)
        # Note: 'mothers_age_at_first_birth'
        cia_pack['mothers_age_at_first_birth'] = get_society(
            data=data, info='mothers_age_at_first_birth', iso3Code=iso3Code)
        # Note: 'nationality'
        cia_pack['nationality'] = get_society(
            data=data, info='nationality', iso3Code=iso3Code)
        # Note: 'net_migration_rate'
        cia_pack['net_migration_rate'] = get_society(
            data=data, info='net_migration_rate', iso3Code=iso3Code)
        # Note: 'obesity'
        cia_pack['obesity'] = get_society(
            data=data, info='obesity', iso3Code=iso3Code)
        # Note: 'physician_density'
        cia_pack['physician_density'] = get_society(
            data=data, info='physician_density', iso3Code=iso3Code)
        # Note: 'population'
        cia_pack['population'] = get_society(
            data=data, info='population', iso3Code=iso3Code)
        # Note: 'population_distribution'
        cia_pack['population_distribution'] = get_society(
            data=data, info='population_distribution', iso3Code=iso3Code)
        # Note: 'population_growth'
        cia_pack['population_growth'] = get_society(
            data=data, info='population_growth', iso3Code=iso3Code)
        # Note: 'religions'
        cia_pack['religions'] = get_society(
            data=data, info='religions', iso3Code=iso3Code)
        # Note: 'sanitation_access'
        cia_pack['sanitation_access'] = get_society(
            data=data, info='sanitation_access', iso3Code=iso3Code)
        # Note: 'school_life_expectancy'
        cia_pack['school_life_expectancy'] = get_society(
            data=data, info='school_life_expectancy', iso3Code=iso3Code)
        # Note: 'sex_ratio'
        cia_pack['sex_ratio'] = get_society(
            data=data, info='sex_ratio', iso3Code=iso3Code)
        # Note: 'tobacco_use'
        cia_pack['tobacco_use'] = get_society(
            data=data, info='tobacco_use', iso3Code=iso3Code)
        # Note: 'fertility_rate'
        cia_pack['fertility_rate'] = get_society(
            data=data, info='fertility_rate', iso3Code=iso3Code)
        # Note: 'people_note'
        cia_pack['people_note'] = get_society(
            data=data, info='people_note', iso3Code=iso3Code)
        # Note: 'urbanization'
        cia_pack['urbanization'] = get_society(
            data=data, info='urbanization', iso3Code=iso3Code)
    else:
        # Note: ''
        pass

    # Return the compiled geography data
    return cia_pack


######################################################################################################################
#   TEST FUNCTION
######################################################################################################################
if __name__ == '__main__':
    country = True
    # ----------------------------------------------------------------------------------------------------------------------------------
    json_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
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
        return_society_data(
            data=data,
            iso3Code=iso3Code
        )
    )
