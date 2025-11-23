#!/usr/bin/env python3
"""
Comprehensive test for ALL society parsers against ALL countries.
Tests each parser against every country JSON file including world.
"""

import json
import os
import sys
import traceback
from pathlib import Path

# Add project to path
sys.path.insert(0, '/home/user/solve_cia')

# Import all parsers
from proj_004_cia.c_03_society.helper.utils.parse_dependency_ratios import parse_dependency_ratios
from proj_004_cia.c_03_society.helper.utils.parse_population import parse_population
from proj_004_cia.c_03_society.helper.utils.parse_ethnic_groups import parse_ethnic_groups
from proj_004_cia.c_03_society.helper.utils.parse_age_structure import parse_age_structure
from proj_004_cia.c_03_society.helper.utils.parse_education_expenditure import parse_education_expenditure
from proj_004_cia.c_03_society.helper.utils.parse_net_migration_rate import parse_net_migration_rate
from proj_004_cia.c_03_society.helper.utils.parse_religions import parse_religions
from proj_004_cia.c_03_society.helper.utils.parse_urbanization import parse_urbanization
from proj_004_cia.c_03_society.helper.utils.parse_sex_ratio import parse_sex_ratio
from proj_004_cia.c_03_society.helper.utils.parse_death_rate import parse_death_rate
from proj_004_cia.c_03_society.helper.utils.parse_obesity import parse_obesity
from proj_004_cia.c_03_society.helper.utils.parse_fertility_rate import parse_fertility_rate
from proj_004_cia.c_03_society.helper.utils.parse_school_life_expectancy import parse_school_life_expectancy
from proj_004_cia.c_03_society.helper.utils.parse_population_growth import parse_population_growth
from proj_004_cia.c_03_society.helper.utils.parse_physician_density import parse_physician_density
from proj_004_cia.c_03_society.helper.utils.parse_infant_mortality import parse_infant_mortality
from proj_004_cia.c_03_society.helper.utils.parse_maternal_mortality import parse_maternal_mortality
from proj_004_cia.c_03_society.helper.utils.parse_reproduction_rate import parse_reproduction_rate
from proj_004_cia.c_03_society.helper.utils.parse_tobacco_use import parse_tobacco_use
from proj_004_cia.c_03_society.helper.utils.parse_health_expenditure import parse_health_expenditure
from proj_004_cia.c_03_society.helper.utils.parse_languages import parse_languages
from proj_004_cia.c_03_society.helper.utils.parse_birth_rate import parse_birth_rate
from proj_004_cia.c_03_society.helper.utils.parse_child_under_5_under_weight import parse_child_under_5_under_weight
from proj_004_cia.c_03_society.helper.utils.parse_life_expectancy_at_birth import parse_life_expectancy_at_birth
from proj_004_cia.c_03_society.helper.utils.parse_mothers_age_at_first_birth import parse_mothers_age_at_first_birth
from proj_004_cia.c_03_society.helper.utils.parse_nationality import parse_nationality
from proj_004_cia.c_03_society.helper.utils.parse_hospital_bed_density import parse_hospital_bed_density
from proj_004_cia.c_03_society.helper.utils.parse_median_age import parse_median_age
from proj_004_cia.c_03_society.helper.utils.parse_literacy import parse_literacy
from proj_004_cia.c_03_society.helper.utils.parse_contraceptive_rate import parse_contraceptive_rate
from proj_004_cia.c_03_society.helper.utils.parse_alcohol import parse_alcohol
from proj_004_cia.c_03_society.helper.utils.parse_child_marriage import parse_child_marriage
from proj_004_cia.c_03_society.helper.utils.parse_population_distribution import parse_population_distribution
from proj_004_cia.c_03_society.helper.utils.parse_major_urban_areas import parse_major_urban_areas
from proj_004_cia.c_03_society.helper.utils.parse_drinking_water_source import parse_drinking_water_source
from proj_004_cia.c_03_society.helper.utils.parse_sanitation_access import parse_sanitation_access
from proj_004_cia.c_03_society.helper.utils.parse_women_married_15_49 import parse_women_married_15_49
from proj_004_cia.c_03_society.helper.utils.parse_demographic_profile import parse_demographic_profile
from proj_004_cia.c_03_society.helper.utils.parse_people_note import parse_people_note
from proj_004_cia.c_03_society.helper.utils.parse_hiv_rate import parse_hiv_rate
from proj_004_cia.c_03_society.helper.utils.parse_hiv_deaths import parse_hiv_deaths
from proj_004_cia.c_03_society.helper.utils.parse_hiv_living_with import parse_hiv_living_with
from proj_004_cia.c_03_society.helper.utils.parse_infectious_diseases import parse_infectious_diseases


# Map parser functions to their CIA field names
PARSER_CONFIG = {
    'parse_population': ('Population', parse_population),
    'parse_nationality': ('Nationality', parse_nationality),
    'parse_ethnic_groups': ('Ethnic groups', parse_ethnic_groups),
    'parse_languages': ('Languages', parse_languages),
    'parse_religions': ('Religions', parse_religions),
    'parse_age_structure': ('Age structure', parse_age_structure),
    'parse_dependency_ratios': ('Dependency ratios', parse_dependency_ratios),
    'parse_median_age': ('Median age', parse_median_age),
    'parse_population_growth': ('Population growth rate', parse_population_growth),
    'parse_birth_rate': ('Birth rate', parse_birth_rate),
    'parse_death_rate': ('Death rate', parse_death_rate),
    'parse_net_migration_rate': ('Net migration rate', parse_net_migration_rate),
    'parse_population_distribution': ('Population distribution', parse_population_distribution),
    'parse_urbanization': ('Urbanization', parse_urbanization),
    'parse_major_urban_areas': ('Major urban areas - population', parse_major_urban_areas),
    'parse_sex_ratio': ('Sex ratio', parse_sex_ratio),
    'parse_mothers_age_at_first_birth': ("Mother's mean age at first birth", parse_mothers_age_at_first_birth),
    'parse_maternal_mortality': ('Maternal mortality ratio', parse_maternal_mortality),
    'parse_infant_mortality': ('Infant mortality rate', parse_infant_mortality),
    'parse_life_expectancy_at_birth': ('Life expectancy at birth', parse_life_expectancy_at_birth),
    'parse_fertility_rate': ('Total fertility rate', parse_fertility_rate),
    'parse_reproduction_rate': ('Gross reproduction rate', parse_reproduction_rate),
    'parse_contraceptive_rate': ('Contraceptive prevalence rate', parse_contraceptive_rate),
    'parse_drinking_water_source': ('Drinking water source', parse_drinking_water_source),
    'parse_sanitation_access': ('Sanitation facility access', parse_sanitation_access),
    'parse_physician_density': ('Physician density', parse_physician_density),
    'parse_hospital_bed_density': ('Hospital bed density', parse_hospital_bed_density),
    'parse_obesity': ('Obesity - adult prevalence rate', parse_obesity),
    'parse_alcohol': ('Alcohol consumption per capita', parse_alcohol),
    'parse_tobacco_use': ('Tobacco use', parse_tobacco_use),
    'parse_child_under_5_under_weight': ('Children under the age of 5 years underweight', parse_child_under_5_under_weight),
    'parse_child_marriage': ('Child marriage', parse_child_marriage),
    'parse_education_expenditure': ('Education expenditures', parse_education_expenditure),
    'parse_literacy': ('Literacy', parse_literacy),
    'parse_school_life_expectancy': ('School life expectancy (primary to tertiary education)', parse_school_life_expectancy),
    'parse_women_married_15_49': ('Currently married women (ages 15-49)', parse_women_married_15_49),
    'parse_health_expenditure': ('Current health expenditure', parse_health_expenditure),
    'parse_demographic_profile': ('Demographic profile', parse_demographic_profile),
    'parse_people_note': ('note', parse_people_note),
    'parse_hiv_rate': ('HIV/AIDS - adult prevalence rate', parse_hiv_rate),
    'parse_hiv_deaths': ('HIV/AIDS - deaths', parse_hiv_deaths),
    'parse_hiv_living_with': ('HIV/AIDS - people living with HIV/AIDS', parse_hiv_living_with),
    'parse_infectious_diseases': ('Major infectious diseases', parse_infectious_diseases),
}


def load_all_countries():
    """Load all country JSON files from all regions."""
    raw_data_path = Path('/home/user/solve_cia/proj_004_cia/_raw_data')
    countries = []

    for json_file in raw_data_path.rglob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                countries.append({
                    'path': str(json_file),
                    'name': json_file.stem,
                    'region': json_file.parent.name,
                    'data': data
                })
        except Exception as e:
            print(f"ERROR loading {json_file}: {e}")

    return countries


def get_society_section(country_data):
    """Extract the People and Society section from country data."""
    if not country_data:
        return {}

    # Try different possible keys
    for key in ['People and Society', 'People', 'Society']:
        if key in country_data:
            return country_data[key]

    return {}


def test_parser(parser_name, field_name, parser_func, countries):
    """Test a single parser against all countries."""
    results = {
        'success': 0,
        'no_data': 0,
        'errors': [],
        'parsed_count': 0
    }

    for country in countries:
        try:
            society = get_society_section(country['data'])

            # Get the field data
            field_data = society.get(field_name, {})

            # Call the parser
            result = parser_func(field_data, country['name'][:3].upper())

            # Check if result is valid (dict returned)
            if isinstance(result, dict):
                results['success'] += 1
                # Check if any actual data was parsed
                has_data = False
                for key, value in result.items():
                    if value and not key.endswith('_note'):
                        if isinstance(value, dict):
                            has_data = any(v is not None for v in value.values())
                        elif isinstance(value, list):
                            has_data = len(value) > 0
                        else:
                            has_data = value is not None
                        if has_data:
                            break
                if has_data:
                    results['parsed_count'] += 1
                else:
                    results['no_data'] += 1
            else:
                results['errors'].append({
                    'country': country['name'],
                    'region': country['region'],
                    'error': f"Invalid return type: {type(result)}"
                })

        except Exception as e:
            results['errors'].append({
                'country': country['name'],
                'region': country['region'],
                'error': str(e),
                'traceback': traceback.format_exc()
            })

    return results


def main():
    print("=" * 80)
    print("COMPREHENSIVE SOCIETY PARSER TEST")
    print("Testing ALL 43 parsers against ALL 262 countries")
    print("=" * 80)
    print()

    # Load all countries
    print("Loading all country JSON files...")
    countries = load_all_countries()
    print(f"Loaded {len(countries)} countries from all regions")
    print()

    # Test each parser
    all_results = {}
    total_parsers = len(PARSER_CONFIG)
    failed_parsers = []

    for idx, (parser_name, (field_name, parser_func)) in enumerate(PARSER_CONFIG.items(), 1):
        print(f"[{idx:2d}/{total_parsers}] Testing {parser_name}...", end=" ")
        results = test_parser(parser_name, field_name, parser_func, countries)
        all_results[parser_name] = results

        if results['errors']:
            print(f"FAILED - {len(results['errors'])} errors")
            failed_parsers.append(parser_name)
        else:
            print(f"OK - {results['parsed_count']}/{len(countries)} with data, {results['no_data']} no data")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    # Summary table
    print(f"{'Parser':<45} {'Success':>8} {'W/Data':>8} {'NoData':>8} {'Errors':>8}")
    print("-" * 80)

    for parser_name, results in all_results.items():
        status = "✓" if not results['errors'] else "✗"
        print(f"{status} {parser_name:<43} {results['success']:>8} {results['parsed_count']:>8} {results['no_data']:>8} {len(results['errors']):>8}")

    print("-" * 80)

    # Overall stats
    total_success = sum(r['success'] for r in all_results.values())
    total_tests = len(countries) * total_parsers
    total_errors = sum(len(r['errors']) for r in all_results.values())

    print(f"Total: {total_success}/{total_tests} tests passed ({total_success/total_tests*100:.2f}%)")
    print(f"Errors: {total_errors}")
    print()

    # Show error details if any
    if failed_parsers:
        print("=" * 80)
        print("ERROR DETAILS")
        print("=" * 80)
        for parser_name in failed_parsers:
            results = all_results[parser_name]
            print(f"\n{parser_name}:")
            for err in results['errors'][:5]:  # Show first 5 errors
                print(f"  - {err['region']}/{err['country']}: {err['error']}")
                if 'traceback' in err:
                    print(f"    Traceback: {err['traceback'][:200]}...")
    else:
        print("ALL PARSERS PASSED! 100% SUCCESS RATE")

    return len(failed_parsers) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
