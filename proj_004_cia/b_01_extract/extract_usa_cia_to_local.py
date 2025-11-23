'''
PURPOSE OF THIS FILE
--------------------
Generate the original CIA metadata for each country by parsing the JSON files from the CIA World Factbook and outputting valid Python files.
Enhanced with region and country filtering capabilities.
'''

#######################################################################################################################
# CORE IMPORTS - proj_004_cia.__logger.logger
# ---------------------------------------------------------------------------------------------------------------------

import os
import json
import logging
from tqdm import tqdm
from typing import Dict, Any, List, Optional
from proj_004_cia.__logger.logger import app_logger
# Import custom modules
from proj_004_cia.a_02_cia_area_codes.utils.cia_code_names import cia_code_names
from proj_004_cia.a_01_cia_to_iso.utils.cia_region_names import cia_region_names


# Import section generators
# proj_004_cia.c_01_intoduction.return_introduction_data
from proj_004_cia.c_01_intoduction.return_introduction_data import return_introduction_data
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.c_05_government.return_government_data import return_government_data
from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.c_07_energy.return_energy_data import return_energy_data
from proj_004_cia.c_08_communications.return_communications_data import return_communications_data
from proj_004_cia.c_09_transportation.return_transportation_data import return_transportation_data
from proj_004_cia.c_10_military.return_military_data import return_military_data
from proj_004_cia.c_11_space.return_space_data import return_space_data
from proj_004_cia.c_12_terrorism.return_terrorism_data import return_terrorism_data
from proj_004_cia.c_13_issues.return_issues_data import return_issues_data

#######################################################################################################################
# UTILITY FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------


def load_json_file(file_path: str) -> Dict[str, Any]:
    """Load a JSON file and return its content as a dictionary."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        if app_logger:
            app_logger.error(f"Error loading JSON file {file_path}: {e}")
        return {}


def write_country_meta_file(file_path: str, variable_name: str, data: Dict[str, Any]):
    """Write the country metadata to a Python file defining a variable."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # Write the variable assignment
            file.write(f'{variable_name} = ')

            # Serialize data to a JSON-formatted string with human-readable characters
            json_string = json.dumps(data, indent=4, ensure_ascii=False)

            # Replace any special apostrophes with regular ones
            # Right single quotation mark → regular apostrophe
            json_string = json_string.replace('\u2019', "'")
            # Left single quotation mark → regular apostrophe
            json_string = json_string.replace('\u2018', "'")
            # Left double quotation mark → regular quote
            json_string = json_string.replace('\u201c', '"')
            # Right double quotation mark → regular quote
            json_string = json_string.replace('\u201d', '"')

            # Write the modified JSON string to the file
            file.write(json_string)
            file.write('\n')  # Ensure there's a newline at the end
    except Exception as e:
        if app_logger:
            app_logger.error(f"Error writing file {file_path}: {e}")


def create_directory(path: str):
    """Create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def validate_region(region: str) -> str:
    """
    Validate and normalize region input.

    Args:
        region: Region name (folder name or display name)

    Returns:
        Normalized region folder name

    Raises:
        ValueError: If region is invalid
    """
    if not region:
        return None

    # Normalize to lowercase for comparison
    region_lower = region.lower()

    # Check if it's a valid folder name (key)
    if region_lower in cia_region_names:
        return region_lower

    # Check if it's a valid display name (value)
    for folder_name, display_name in cia_region_names.items():
        if display_name.lower() == region_lower:
            return folder_name

    # If not found, raise error with available options
    available_regions = list(cia_region_names.keys()) + \
        list(cia_region_names.values())
    raise ValueError(
        f"Invalid region '{region}'. Available regions are: {', '.join(sorted(available_regions))}"
    )


def validate_countries(countries: List[str]) -> List[str]:
    """
    Validate country ISO3 codes.

    Args:
        countries: List of ISO3 country codes

    Returns:
        Validated list of ISO3 codes

    Raises:
        ValueError: If any country code is invalid
    """
    if not countries:
        return []

    # Get all valid ISO3 codes
    valid_iso3_codes = {info.get(
        'iso3Code') for info in cia_code_names.values() if info.get('iso3Code')}

    # Check each country
    invalid_countries = []
    for country in countries:
        if country not in valid_iso3_codes:
            invalid_countries.append(country)

    if invalid_countries:
        raise ValueError(
            f"Invalid country codes: {', '.join(invalid_countries)}. "
            f"Please use valid ISO3 codes (e.g., USA, ESP, FRA)."
        )

    return countries


def get_countries_in_region(region_folder: str) -> List[str]:
    """
    Get all ISO3 codes for countries in a specific region.

    Args:
        region_folder: Region folder name (e.g., 'europe')

    Returns:
        List of ISO3 codes for countries in that region
    """
    countries_in_region = []
    for cia_code, country_info in cia_code_names.items():
        if country_info.get('region_name', '').lower() == cia_region_names.get(region_folder, '').lower():
            iso3_code = country_info.get('iso3Code')
            if iso3_code:
                countries_in_region.append(iso3_code)

    return countries_in_region


def get_cia_codes_for_iso3_codes(iso3_codes: List[str]) -> List[str]:
    """
    Convert ISO3 codes to CIA codes for file processing.

    Args:
        iso3_codes: List of ISO3 country codes

    Returns:
        List of CIA codes corresponding to the ISO3 codes
    """
    cia_codes = []
    for cia_code, country_info in cia_code_names.items():
        if country_info.get('iso3Code') in iso3_codes:
            cia_codes.append(cia_code)

    return cia_codes


def determine_target_countries(countries: Optional[List[str]] = None, region: Optional[str] = None) -> List[str]:
    """
    Determine which countries to process based on filters.

    Args:
        countries: Optional list of ISO3 country codes
        region: Optional region name

    Returns:
        List of ISO3 codes to process
    """
    target_countries = set()

    # Add countries from region if specified
    if region:
        validated_region = validate_region(region)
        region_countries = get_countries_in_region(validated_region)
        target_countries.update(region_countries)

        if app_logger:
            app_logger.info(
                f"Added {len(region_countries)} countries from region '{cia_region_names[validated_region]}'")

    # Add specific countries if specified
    if countries:
        validated_countries = validate_countries(countries)
        target_countries.update(validated_countries)

        if app_logger:
            app_logger.info(
                f"Added {len(validated_countries)} specific countries: {', '.join(validated_countries)}")

    # If neither specified, return all countries
    if not countries and not region:
        all_countries = [info.get(
            'iso3Code') for info in cia_code_names.values() if info.get('iso3Code')]
        target_countries.update(all_countries)

        if app_logger:
            app_logger.info("No filters specified - processing all countries")

    return sorted(list(target_countries))


#######################################################################################################################
# MAIN FUNCTION
# ---------------------------------------------------------------------------------------------------------------------

def extract_usa_cia_to_local(countries: Optional[List[str]] = None,
                             region: Optional[str] = None,
                             enable_performance_monitoring: bool = True,
                             skip_sections: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Generate original CIA metadata for each country by parsing the JSON files and writing Python files.

    Args:
        countries: Optional list of ISO3 country codes to process (e.g., ['USA', 'ESP', 'FRA'])
        region: Optional region name (folder name like 'europe' or display name like 'Europe')
        enable_performance_monitoring: Whether to track processing time and performance metrics
        skip_sections: Optional list of section names to skip during processing

    Returns:
        Dictionary with processing summary including section-level statistics

    Examples:
        # Process all countries
        extract_usa_cia_to_local()

        # Process specific countries
        extract_usa_cia_to_local(countries=['USA', 'ESP', 'FRA'])

        # Process all countries in Europe
        extract_usa_cia_to_local(region='europe')

        # Process all European countries plus USA and Japan
        extract_usa_cia_to_local(countries=['USA', 'JPN'], region='Europe')

        # Process with specific sections skipped
        extract_usa_cia_to_local(countries=['USA'], skip_sections=['terrorism', 'military'])
    """

    import time
    start_time = time.time()

    if app_logger:
        app_logger.agent("🚀 Starting CIA metadata extraction process",
                         agent_name="CIAExtractor", action="initialize")

    try:
        # Determine target countries based on filters
        target_iso3_codes = determine_target_countries(countries, region)

        if not target_iso3_codes:
            if app_logger:
                app_logger.warning("No countries to process after filtering")
            return {"status": "no_countries", "processed": 0, "errors": 0}

        if app_logger:
            app_logger.info(
                f"Processing {len(target_iso3_codes)} countries: {', '.join(target_iso3_codes[:10])}{'...' if len(target_iso3_codes) > 10 else ''}")

        # Setup directories
        raw_data_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'
        local_usa_cia_save_dir = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_data_per_country'

        # Initialize tracking variables
        original_cia_meta = {}
        processed_count = 0
        error_count = 0
        section_stats = {section: {'success': 0, 'errors': 0} for section, _ in [
            ("introduction", None), ("geography", None), ("government", None),
            ("society", None), ("economy", None), ("environment", None),
            ("energy", None), ("communications", None), ("transportation", None),
            ("military", None), ("space", None), ("terrorism", None), ("issues", None)
        ]}

        # Define non-country regions and special handling regions
        non_country_regions = ['antarctica', 'meta', 'oceans']
        special_regions = ['world']  # Regions that need different processing

        # Get all region directories
        all_directories = [d for d in os.listdir(
            raw_data_folder) if os.path.isdir(os.path.join(raw_data_folder, d))]

        # Process each region
        for cia_region in tqdm(all_directories, desc='Processing Regions'):
            if cia_region in non_country_regions:
                if app_logger:
                    app_logger.info(
                        f"Skipping non-country region: {cia_region}")
                continue

            # Handle World data specially (iso3Code = 'WLD')
            if cia_region in special_regions:
                if app_logger:
                    app_logger.agent(f"Processing special region: {cia_region}",
                                     agent_name="WorldDataProcessor", action="process_global_data")
                # World data processing logic would go here
                continue

            region_name = cia_region_names.get(cia_region, 'Unknown Region')
            cia_region_folder = os.path.join(raw_data_folder, cia_region)
            all_files = [f for f in os.listdir(
                cia_region_folder) if f.endswith('.json')]

            # Filter files to only process target countries
            files_to_process = []
            for file in all_files:
                cia_file_code = file.replace('.json', '')
                country_info = cia_code_names.get(cia_file_code, {})
                iso3_code = country_info.get('iso3Code')

                if iso3_code in target_iso3_codes:
                    files_to_process.append(file)

            if not files_to_process:
                if app_logger:
                    app_logger.debug(
                        f"No target countries found in region {region_name}")
                continue

            # Process each country's JSON file in the region
            for file in tqdm(files_to_process, desc=f'Processing Countries in {region_name}'):
                try:
                    cia_file_code = file.replace('.json', '')
                    country_info = cia_code_names.get(cia_file_code, {})

                    if not country_info:
                        if app_logger:
                            app_logger.warning(
                                f"No country info found for code: {cia_file_code}")
                        error_count += 1
                        continue

                    iso3Code = country_info.get('iso3Code')
                    file_path = os.path.join(cia_region_folder, file)
                    data = load_json_file(file_path)

                    if not data:
                        if app_logger:
                            app_logger.error(
                                f"Data is empty for file: {file_path}")
                        error_count += 1
                        continue

                    # Build the country metadata dictionary
                    country_cia_meta = {
                        'country_name': country_info.get('country_name', 'Unknown Country'),
                        'region': region_name,
                        'introduction': {},
                        'geography': {},
                        'society': {},
                        'environment': {},
                        'government': {},
                        'economy': {},
                        'energy': {},
                        'communications': {},
                        'transportation': {},
                        'military': {},
                        'space': {},
                        'terrorism': {},
                        'issues': {}
                    }

                    # List of sections to be updated (prioritized by coverage and importance)
                    all_sections = [
                        # High coverage, simple
                        ("introduction", return_introduction_data),
                        # High coverage, moderate complexity
                        ("geography", return_geography_data),
                        # High coverage, important for analysis

                        ("government", return_government_data),
                        # High coverage, demographic data
                        # ("society", return_society_data),
                        # High coverage, critical for analysis
                        # ("economy", return_economy_data),
                        # Growing importance
                        # ("environment", return_environment_data),
                        # Strategic importance
                        # ("energy", return_energy_data),
                        # Infrastructure data
                        # ("communications", return_communications_data),
                        # Infrastructure data
                        # ("transportation", return_transportation_data),
                        # Security analysis
                        # ("military", return_military_data),
                        # Future capabilities
                        # ("space", return_space_data),
                        # Security analysis
                        # ("terrorism", return_terrorism_data),
                        # International relations
                        # ("issues", return_issues_data)
                    ]

                    # Filter out skipped sections
                    sections = [(name, func) for name, func in all_sections
                                if not skip_sections or name not in skip_sections]

                    # Update sections in a loop with detailed tracking
                    for section_name, function in sections:
                        try:
                            section_data = function(data, iso3Code)
                            country_cia_meta[section_name].update(section_data)
                            section_stats[section_name]['success'] += 1

                            if app_logger:
                                app_logger.data(f"Successfully processed {section_name}",
                                                source=f"{iso3Code}_{section_name}",
                                                records=len(section_data) if isinstance(section_data, dict) else 1)
                        except Exception as e:
                            section_stats[section_name]['errors'] += 1
                            if app_logger:
                                app_logger.error(
                                    f"Error updating '{section_name}' section for {iso3Code} - {country_info.get('country_name', 'Unknown Country')} - {cia_file_code} - {cia_region}: {e}")
                            error_count += 1

                    # Write the country metadata to a Python file
                    country_variable_name = f'{iso3Code}_cia_meta'
                    country_file_name = f'{country_variable_name}.py'
                    country_file_path = os.path.join(
                        local_usa_cia_save_dir, country_file_name)
                    write_country_meta_file(
                        country_file_path, country_variable_name, country_cia_meta)

                    # Add to the main metadata dictionary
                    original_cia_meta[iso3Code] = country_cia_meta
                    processed_count += 1

                    if app_logger:
                        app_logger.success(
                            f"✅ Processed {country_info.get('country_name', 'Unknown Country')} ({iso3Code})")
                        if enable_performance_monitoring:
                            processing_time = time.time() - start_time
                            app_logger.performance(f"Country processing",
                                                   duration=processing_time * 1000,
                                                   operation=f"process_{iso3Code}")

                except Exception as e:
                    if app_logger:
                        app_logger.error(
                            f"Unexpected error processing file {file}: {e}")
                    error_count += 1

        # Final summary with detailed analytics
        total_time = time.time() - start_time

        if app_logger:
            app_logger.agent(f"🎉 CIA metadata extraction completed!",
                             agent_name="CIAExtractor", action="complete")
            app_logger.business(f"📊 Summary: {processed_count} countries processed, {error_count} errors",
                                division="data_extraction", function="cia_metadata")

            if enable_performance_monitoring:
                app_logger.performance(f"Total extraction process",
                                       duration=total_time * 1000,
                                       operation="full_extraction")

            # Log section-level statistics
            for section, stats in section_stats.items():
                if stats['success'] > 0 or stats['errors'] > 0:
                    success_rate = (stats['success'] / (stats['success'] + stats['errors'])) * 100 if (
                        stats['success'] + stats['errors']) > 0 else 0
                    app_logger.data(f"Section {section}: {stats['success']} success, {stats['errors']} errors ({success_rate:.1f}% success rate)",
                                    source=f"section_{section}", records=stats['success'])

        return {
            "status": "completed",
            "processed": processed_count,
            "errors": error_count,
            "countries": list(original_cia_meta.keys()),
            "section_statistics": section_stats,
            "success_rate": (processed_count / (processed_count + error_count)) * 100 if (processed_count + error_count) > 0 else 0,
            "processing_time_seconds": total_time,
            "sections_processed": [name for name, _ in sections] if 'sections' in locals() else []
        }

    except Exception as e:
        if app_logger:
            app_logger.critical(
                f"Critical error in extract_usa_cia_to_local: {e}")
        raise


#######################################################################################################################
# ENTRY POINT
# ---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # Example usage demonstrations

    # Process all countries (original behavior)
    # result = extract_usa_cia_to_local()

    # Process specific countries
    result = extract_usa_cia_to_local(countries=['USA', 'ESP', 'FRA', 'NGA'])

    # Process all countries in Europe
    # result = extract_usa_cia_to_local(region='europe')

    # Process all European countries plus USA and Japan
    # result = extract_usa_cia_to_local(countries=['USA', 'JPN'], region='Europe')

    # For testing, run with default behavior
    # extract_usa_cia_to_local()
