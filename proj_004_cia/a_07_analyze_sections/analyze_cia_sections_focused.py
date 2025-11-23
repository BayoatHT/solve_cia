######################################################################################################################
#   CIA SECTION-SPECIFIC ANALYSIS GENERATOR
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
import re
from collections import defaultdict, Counter
from typing import Dict, List, Any
from impact_titan.impact_3_data._config._DATA_CONFIG import DataConfig
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
#   CORE CONFIGURATION
# ---------------------------------------------------------------------------------------------------------------------

# First-level properties with their normalized names
MAIN_SECTIONS = {
    "Military and Security": "military_and_security",
    "Transportation": "transportation",
    "Terrorism": "terrorism",
    "Geography": "geography",
    "Government": "government",
    "Energy": "energy",
    "Environment": "environment",
    "Economy": "economy",
    "Transnational Issues": "transnational_issues",
    "Introduction": "introduction",
    "People and Society": "people_and_society",
    "Space": "space",
    "Communications": "communications"
}

######################################################################################################################
#   SECTION-SPECIFIC ANALYSIS FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------


def analyze_cia_sections_focused():
    """
    Generate focused analysis reports for each of the 13 main CIA JSON sections
    """

    # ESTABLISH PATHS
    analysis_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\a_07_analyze_sections\analysis_folder'
    raw_data_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'

    # ANALYSIS CONTAINERS - one per section
    section_analyses = {}
    for section_display_name, section_key in MAIN_SECTIONS.items():
        section_analyses[section_key] = {
            'section_display_name': section_display_name,
            'properties': defaultdict(dict),
            'parsing_requirements': defaultdict(list),
            'data_types': defaultdict(Counter),
            'complexity_scores': defaultdict(int),
            'coverage_stats': defaultdict(dict),
            'sample_values': defaultdict(list),
            'helper_functions_needed': set(),
            'countries_with_section': set(),
            'total_properties': 0
        }

    # PROCESSING VARIABLES
    total_files = 0
    non_country_regions = ['antarctica', 'meta', 'oceans']

    # PROCESS ALL FILES
    for cia_region in os.listdir(raw_data_folder):
        if cia_region in non_country_regions:
            continue

        cia_region_folder = os.path.join(raw_data_folder, cia_region)
        if not os.path.isdir(cia_region_folder):
            continue

        for file in os.listdir(cia_region_folder):
            if not file.endswith('.json'):
                continue

            file_path = os.path.join(cia_region_folder, file)
            country_code = file.replace('.json', '')

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Analyze each main section in this file
                analyze_file_sections(data, section_analyses, country_code)
                total_files += 1

            except Exception as e:
                print(f"Error processing {file}: {e}")

    # GENERATE SECTION REPORTS
    for section_key, analysis in section_analyses.items():
        analysis['total_files_analyzed'] = total_files
        generate_section_report(analysis, section_key, analysis_folder)

    # GENERATE MASTER SUMMARY
    generate_master_summary(section_analyses, analysis_folder, total_files)

    return section_analyses


def analyze_file_sections(data: Dict, section_analyses: Dict, country_code: str):
    """
    Analyze each main section within a single JSON file
    """
    for section_display_name, section_key in MAIN_SECTIONS.items():
        if section_display_name in data:
            section_data = data[section_display_name]
            section_analyses[section_key]['countries_with_section'].add(
                country_code)

            # Analyze this section's structure
            analyze_section_structure(
                section_data,
                section_analyses[section_key],
                country_code,
                section_key
            )


def analyze_section_structure(section_data: Dict, analysis: Dict, country_code: str, section_key: str):
    """
    Analyze the structure of a specific section
    """
    if not isinstance(section_data, dict):
        return

    for property_name, property_data in section_data.items():
        property_key = normalize_property_name(property_name)

        # Initialize property analysis if not exists
        if property_key not in analysis['properties']:
            analysis['properties'][property_key] = {
                'display_name': property_name,
                'countries_with_property': set(),
                'data_patterns': set(),
                'parsing_challenges': Counter(),  # Changed to Counter
                'sample_values': [],
                'complexity_score': 0,
                'function_name': f"parse_{section_key}_{property_key}",
                'helper_functions': []
            }

        # Add country to property coverage
        analysis['properties'][property_key]['countries_with_property'].add(
            country_code)

        # Analyze the property data
        analyze_property_data(
            property_data, analysis['properties'][property_key], analysis)

    # Update total properties count
    analysis['total_properties'] = len(analysis['properties'])


def analyze_property_data(property_data: Any, property_analysis: Dict, section_analysis: Dict):
    """
    Analyze individual property data for patterns and requirements
    """
    # Store sample values (limit to 3)
    if len(property_analysis['sample_values']) < 3:
        property_analysis['sample_values'].append(property_data)

    # Analyze based on data type
    data_type = type(property_data).__name__

    if isinstance(property_data, dict):
        analyze_dict_property(
            property_data, property_analysis, section_analysis)
    elif isinstance(property_data, str):
        analyze_string_property(
            property_data, property_analysis, section_analysis)
    elif isinstance(property_data, list):
        analyze_list_property(
            property_data, property_analysis, section_analysis)
    elif isinstance(property_data, (int, float)):
        analyze_numeric_property(
            property_data, property_analysis, section_analysis)


def analyze_dict_property(property_data: Dict, property_analysis: Dict, section_analysis: Dict):
    """
    Analyze dictionary-type properties with comprehensive pattern detection
    """
    property_analysis['data_patterns'].add('nested_dictionary')
    property_analysis['complexity_score'] += calculate_dict_complexity(
        property_data)

    # Detailed analysis of dictionary structure
    keys = list(property_data.keys())

    # Check for common nested patterns
    if any(key in ['text', 'note'] for key in keys):
        property_analysis['parsing_challenges']['text_note_extraction'] += 1
        section_analysis['helper_functions_needed'].add(
            'extract_text_and_note')

    # Check for territorial subdivisions (HTML em tags)
    territorial_found = False
    for value in property_data.values():
        if isinstance(value, str) and '<em>' in value:
            territorial_found = True
            break
    if territorial_found:
        property_analysis['parsing_challenges']['territorial_subdivisions'] += 1
        section_analysis['helper_functions_needed'].add(
            'parse_territorial_subdivisions')

    # Check for multi-year time series data
    year_keys = [k for k in keys if re.search(r'\b(19|20)\d{2}\b', k)]
    if len(year_keys) >= 3:
        property_analysis['parsing_challenges']['time_series_data'] += 1
        section_analysis['helper_functions_needed'].add('parse_time_series')
        property_analysis['data_patterns'].add(
            f'time_series_{len(year_keys)}_years')

    # Check for nested sub-properties
    nested_dicts = sum(1 for v in property_data.values()
                       if isinstance(v, dict))
    if nested_dicts > 0:
        property_analysis['data_patterns'].add(
            f'nested_subdicts_{nested_dicts}')
        if nested_dicts > 3:
            property_analysis['parsing_challenges']['complex_nesting'] += 1

    # Check for mixed data types in values
    value_types = set(type(v).__name__ for v in property_data.values())
    if len(value_types) > 2:
        property_analysis['parsing_challenges']['mixed_value_types'] += 1
        property_analysis['data_patterns'].add(
            f'mixed_types_{len(value_types)}')

    # Check for key patterns that suggest specific parsing needs
    if any(key.lower().endswith(('rate', 'percentage', 'percent')) for key in keys):
        property_analysis['parsing_challenges']['percentage_data'] += 1
        section_analysis['helper_functions_needed'].add('normalize_percentage')

    if any(key.lower().endswith(('total', 'sum', 'amount')) for key in keys):
        property_analysis['data_patterns'].add('aggregated_data')

    # Check for coordinate-like patterns in keys
    coord_pattern = r'(lat|lon|latitude|longitude|north|south|east|west|coordinates)'
    if any(re.search(coord_pattern, key.lower()) for key in keys):
        property_analysis['parsing_challenges']['coordinate_data'] += 1
        section_analysis['helper_functions_needed'].add('parse_coordinates')


def analyze_string_property(property_data: str, property_analysis: Dict, section_analysis: Dict):
    """
    Analyze string-type properties with comprehensive pattern detection
    """
    property_analysis['data_patterns'].add('string_value')

    # Length-based patterns
    text_length = len(property_data)
    if text_length > 1000:
        property_analysis['data_patterns'].add('very_long_text')
        property_analysis['parsing_challenges']['long_text_processing'] += 1
    elif text_length > 300:
        property_analysis['data_patterns'].add('long_text')
    elif text_length < 10:
        property_analysis['data_patterns'].add('short_text')

    # Comprehensive pattern detection
    patterns = {
        # HTML and markup
        'html_tags': r'<[^>]+>',
        'html_entities': r'&[a-zA-Z]+;|&#\d+;',
        'strong_tags': r'<strong>.*?</strong>',
        'em_tags': r'<em>.*?</em>',
        'br_tags': r'<br\s*/?>',

        # Numeric patterns
        'percentage': r'\d+\.?\d*\s*%',
        'decimal_numbers': r'\d+\.\d+',
        'large_numbers': r'\d{1,3}(,\d{3})+',
        'scientific_notation': r'\d+\.?\d*[eE][+-]?\d+',
        'negative_numbers': r'-\d+\.?\d*',
        'numeric_range': r'\d+\.?\d*\s*[-–—]\s*\d+\.?\d*',
        'years_range': r'\b(19|20)\d{2}\s*[-–—]\s*(19|20)\d{2}\b',

        # Currency and financial
        'currency_symbols': r'[\$€£¥₹¢]',
        'financial_amounts': r'\d+\.\d+\s*(million|billion|trillion|thousand)',
        'currency_codes': r'\b[A-Z]{3}\b.*\d',

        # Geographic and coordinates
        'coordinates_dms': r'\d+\s*°?\s*\d+\s*\'?\s*\d*\.?\d*"?\s*[NSEW]',
        'coordinates_decimal': r'-?\d+\.\d+\s*[°]?\s*[NSEW]?',
        'lat_lon_pattern': r'\d+\s+\d+\s+[NS],?\s*\d+\s+\d+\s+[EW]',
        'elevation': r'\d+\.?\d*\s*(m|meters|ft|feet|km)',

        # Date and time patterns
        'date_full': r'\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{4}',
        'date_year_only': r'\b(19|20)\d{2}\b',
        'date_month_year': r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(19|20)\d{2}\b',
        'time_pattern': r'\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?',

        # List and delimiter patterns
        'semicolon_list': r'[^;]+;[^;]+',
        'comma_list': r'[^,]+,[^,]+',
        'bullet_points': r'[\u2022\u2023\u25E6\u2043\u2219]|\*\s+',
        'numbered_list': r'\d+\.\s+\w+',
        'parenthetical_list': r'\([^)]+\)',

        # Language and text patterns
        'non_ascii': r'[^\x00-\x7F]',
        'all_caps': r'\b[A-Z]{3,}\b',
        'acronyms': r'\b[A-Z]{2,}(?:\.[A-Z]{2,})*\b',
        'phone_numbers': r'[\+]?[1-9]?[\s\-\(\)]?\d{1,4}[\s\-\(\)]?\d{1,4}[\s\-\(\)]?\d{4,10}',
        'email_pattern': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'url_pattern': r'https?://[^\s]+',

        # Measurement units
        'area_units': r'\d+\.?\d*\s*(sq\s*km|square\s*kilometers|hectares|acres)',
        'weight_units': r'\d+\.?\d*\s*(kg|kilograms|tons|tonnes|pounds|lbs)',
        'volume_units': r'\d+\.?\d*\s*(liters|gallons|cubic\s*meters|barrels)',
        'distance_units': r'\d+\.?\d*\s*(km|kilometers|miles|meters)',

        # Special formatting
        'newlines': r'\n',
        'multiple_spaces': r'\s{2,}',
        'special_quotes': r'[""''‚„]',
        'unicode_chars': r'[\u2000-\u206F\u2E00-\u2E7F\\!"#$%&\'()*+,\-.\/:;<=>?@\[\]^_`{|}~]',

        # Content-specific patterns
        'population_data': r'\d+\.?\d*\s*(million|billion|thousand)?\s*people',
        'country_names': r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
        'organization_abbrev': r'\b[A-Z]+\b(?:\s*\([^)]+\))?',
    }

    # Apply pattern detection and count instances
    found_patterns = {}
    for pattern_name, pattern_regex in patterns.items():
        matches = re.findall(pattern_regex, property_data, re.IGNORECASE)
        if matches:
            property_analysis['data_patterns'].add(pattern_name)
            found_patterns[pattern_name] = len(matches)
            # Cap complexity contribution
            property_analysis['complexity_score'] += min(len(matches), 3)

    # Map patterns to parsing challenges and helper functions
    challenge_mapping = {
        'html_tags': ('html_tag_removal', 'clean_html_content'),
        'html_entities': ('html_entity_decoding', 'decode_html_entities'),
        'strong_tags': ('note_extraction', 'extract_notes'),
        'em_tags': ('territorial_parsing', 'parse_territorial_subdivisions'),
        'percentage': ('percentage_normalization', 'normalize_percentage'),
        'currency_symbols': ('currency_normalization', 'normalize_currency'),
        'financial_amounts': ('financial_parsing', 'parse_financial_amounts'),
        'coordinates_dms': ('coordinate_parsing', 'parse_coordinates'),
        'coordinates_decimal': ('coordinate_parsing', 'parse_coordinates'),
        'lat_lon_pattern': ('coordinate_parsing', 'parse_coordinates'),
        'date_full': ('date_parsing', 'parse_date_range'),
        'years_range': ('date_range_parsing', 'parse_year_range'),
        'numeric_range': ('range_extraction', 'extract_numeric_range'),
        'semicolon_list': ('list_splitting', 'split_delimited_list'),
        'comma_list': ('list_splitting', 'split_delimited_list'),
        'non_ascii': ('unicode_handling', 'normalize_unicode'),
        'area_units': ('unit_conversion', 'normalize_area_units'),
        'weight_units': ('unit_conversion', 'normalize_weight_units'),
        'newlines': ('multiline_processing', 'process_multiline_text'),
    }

    for pattern_name, count in found_patterns.items():
        if pattern_name in challenge_mapping:
            challenge, helper = challenge_mapping[pattern_name]
            property_analysis['parsing_challenges'][challenge] += count
            section_analysis['helper_functions_needed'].add(helper)


def analyze_list_property(property_data: List, property_analysis: Dict, section_analysis: Dict):
    """
    Analyze list-type properties with detailed content analysis
    """
    property_analysis['data_patterns'].add('list_value')

    if not property_data:
        property_analysis['data_patterns'].add('empty_list')
        return

    list_length = len(property_data)
    property_analysis['data_patterns'].add(f'list_length_{list_length}')

    # Analyze item types and consistency
    item_types = [type(item).__name__ for item in property_data]
    unique_types = set(item_types)

    if len(unique_types) > 1:
        property_analysis['parsing_challenges']['mixed_type_list'] += 1
        property_analysis['complexity_score'] += 2
        property_analysis['data_patterns'].add(
            f'mixed_types_{len(unique_types)}')
    else:
        property_analysis['data_patterns'].add(
            f'homogeneous_{list(unique_types)[0]}')

    # Analyze content patterns for different item types
    if 'str' in unique_types:
        string_items = [
            item for item in property_data if isinstance(item, str)]
        # Check for common string patterns in list items
        if any('<' in item and '>' in item for item in string_items):
            property_analysis['parsing_challenges']['html_in_list_items'] += 1
            section_analysis['helper_functions_needed'].add(
                'clean_html_content')

        if any(re.search(r'\d+\.?\d*%', item) for item in string_items):
            property_analysis['parsing_challenges']['percentage_in_list'] += 1
            section_analysis['helper_functions_needed'].add(
                'normalize_percentage')

        # Check for nested delimited content
        if any(',' in item or ';' in item for item in string_items):
            property_analysis['parsing_challenges']['nested_delimiters'] += 1

    # Check for nested structures
    nested_dicts = sum(1 for item in property_data if isinstance(item, dict))
    nested_lists = sum(1 for item in property_data if isinstance(item, list))

    if nested_dicts > 0:
        property_analysis['parsing_challenges']['nested_dict_in_list'] += nested_dicts
        property_analysis['complexity_score'] += nested_dicts
        property_analysis['data_patterns'].add(
            f'contains_{nested_dicts}_dicts')

    if nested_lists > 0:
        property_analysis['parsing_challenges']['nested_list_structures'] += nested_lists
        property_analysis['complexity_score'] += nested_lists
        property_analysis['data_patterns'].add(
            f'contains_{nested_lists}_sublists')

    # Analyze numeric patterns in lists
    if 'int' in unique_types or 'float' in unique_types:
        numeric_items = [
            item for item in property_data if isinstance(item, (int, float))]
        if numeric_items:
            property_analysis['data_patterns'].add('numeric_list')
            # Check for time series (years)
            if all(isinstance(item, int) and 1900 <= item <= 2100 for item in numeric_items):
                property_analysis['data_patterns'].add('year_sequence')
            # Check for large number variations
            if max(numeric_items) / min(numeric_items) > 1000:
                property_analysis['parsing_challenges']['wide_numeric_range'] += 1


def analyze_numeric_property(property_data: float, property_analysis: Dict, section_analysis: Dict):
    """
    Analyze numeric-type properties
    """
    property_analysis['data_patterns'].add('numeric_value')

    if isinstance(property_data, int):
        property_analysis['data_patterns'].add('integer')
    else:
        property_analysis['data_patterns'].add('decimal')


def calculate_dict_complexity(data: Dict, depth: int = 0) -> int:
    """
    Calculate complexity score for nested dictionaries
    """
    if depth > 5:  # Prevent infinite recursion
        return depth

    complexity = len(data)
    for value in data.values():
        if isinstance(value, dict):
            complexity += calculate_dict_complexity(value, depth + 1)
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            complexity += sum(calculate_dict_complexity(item, depth + 1)
                              for item in value if isinstance(item, dict))

    return complexity


def normalize_property_name(property_name: str) -> str:
    """
    Normalize property names to follow naming convention
    """
    # Convert to lowercase and replace spaces/special chars with underscores
    normalized = re.sub(r'[^a-zA-Z0-9]+', '_', property_name.lower())
    # Remove leading/trailing underscores
    normalized = normalized.strip('_')
    # Replace multiple underscores with single
    normalized = re.sub(r'_+', '_', normalized)
    return normalized

######################################################################################################################
#   REPORT GENERATION FUNCTIONS
######################################################################################################################


def generate_section_report(analysis: Dict, section_key: str, analysis_folder: str):
    """
    Generate a focused report for a specific section
    """
    # Create section-specific folder
    utils_folder = analysis_folder
    section_folder = os.path.join(utils_folder, section_key)
    os.makedirs(section_folder, exist_ok=True)

    report = {
        'section_info': {
            'section_key': section_key,
            'display_name': analysis['section_display_name'],
            'total_files_analyzed': analysis['total_files_analyzed'],
            'countries_with_section': len(analysis['countries_with_section']),
            'coverage_percentage': (len(analysis['countries_with_section']) / analysis['total_files_analyzed']) * 100,
            'total_properties': analysis['total_properties']
        },
        'parsing_requirements': {
            'main_extractor_function': f"return_{section_key}_data",
            'helper_function': f"get_{section_key}",
            'total_parser_functions_needed': len(analysis['properties']),
            'helper_functions_needed': list(analysis['helper_functions_needed'])
        },
        'properties': {},
        'implementation_priority': []
    }

    # Process each property
    for prop_key, prop_data in analysis['properties'].items():
        countries_with_prop = len(prop_data['countries_with_property'])
        coverage_percent = (countries_with_prop /
                            analysis['total_files_analyzed']) * 100

        property_info = {
            'display_name': prop_data['display_name'],
            'function_name': prop_data['function_name'],
            'coverage_percentage': coverage_percent,
            'countries_with_property': countries_with_prop,
            'complexity_score': prop_data['complexity_score'],
            'data_patterns': list(prop_data['data_patterns']),
            # Convert Counter to dict
            'parsing_challenges': dict(prop_data['parsing_challenges']),
            # Limit sample values
            'sample_values': prop_data['sample_values'][:2],
            'priority_score': coverage_percent * 10 - prop_data['complexity_score']
        }

        report['properties'][prop_key] = property_info

        # Add to implementation priority
        report['implementation_priority'].append({
            'property_key': prop_key,
            'function_name': prop_data['function_name'],
            'priority_score': property_info['priority_score'],
            'coverage_percentage': coverage_percent,
            'complexity_score': prop_data['complexity_score']
        })

    # Sort implementation priority
    report['implementation_priority'].sort(
        key=lambda x: x['priority_score'], reverse=True)

    # Save section report
    with open(os.path.join(section_folder, f'cia_{section_key}_analysis.json'), 'w', encoding='utf-8') as f:
        # Convert sets to lists for JSON serialization
        json_report = convert_sets_to_lists(report)
        json.dump(json_report, f, indent=2, ensure_ascii=False)

    # Generate text summary
    generate_section_text_summary(report, section_key, section_folder)


def generate_section_text_summary(report: Dict, section_key: str, section_folder: str):
    """
    Generate a human-readable text summary for a section
    """
    summary = []
    summary.append("=" * 80)
    summary.append(
        f"CIA {report['section_info']['display_name'].upper()} SECTION ANALYSIS")
    summary.append("=" * 80)
    summary.append("")

    # Section overview
    info = report['section_info']
    summary.append("SECTION OVERVIEW:")
    summary.append(
        f"  Coverage: {info['coverage_percentage']:.1f}% ({info['countries_with_section']}/{info['total_files_analyzed']} countries)")
    summary.append(f"  Properties: {info['total_properties']}")
    summary.append("")

    # Implementation requirements
    req = report['parsing_requirements']
    summary.append("IMPLEMENTATION REQUIREMENTS:")
    summary.append(f"  Main Extractor: {req['main_extractor_function']}()")
    summary.append(f"  Helper Function: {req['helper_function']}()")
    summary.append(
        f"  Parser Functions: {req['total_parser_functions_needed']}")
    summary.append(
        f"  Utility Functions: {len(req['helper_functions_needed'])}")
    if req['helper_functions_needed']:
        summary.append("  Utilities Needed:")
        for helper in req['helper_functions_needed']:
            summary.append(f"    - {helper}()")
    summary.append("")

    # High priority properties
    summary.append("HIGH PRIORITY PROPERTIES (>50% coverage):")
    high_priority = [p for p in report['implementation_priority']
                     if p['coverage_percentage'] > 50]
    for prop in high_priority[:10]:
        prop_info = report['properties'][prop['property_key']]
        challenges = ', '.join([f"{k}({v})" for k, v in prop_info['parsing_challenges'].items(
        )]) if prop_info['parsing_challenges'] else 'None'
        summary.append(
            f"  {prop['function_name']}: {prop['coverage_percentage']:.1f}% | Challenges: {challenges}")
    summary.append("")

    # Complex properties
    summary.append("COMPLEX PROPERTIES (high parsing difficulty):")
    complex_props = sorted(report['implementation_priority'],
                           key=lambda x: x['complexity_score'], reverse=True)
    for prop in complex_props[:5]:
        if prop['complexity_score'] > 3:
            prop_info = report['properties'][prop['property_key']]
            patterns = ', '.join(prop_info['data_patterns'])
            summary.append(
                f"  {prop['function_name']}: Score {prop['complexity_score']} | Patterns: {patterns}")

    # Save text summary
    with open(os.path.join(section_folder, f'cia_{section_key}_summary.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary))


def generate_master_summary(section_analyses: Dict, analysis_folder: str, total_files: int):
    """
    Generate a master summary across all sections
    """
    utils_folder = analysis_folder

    master_summary = {
        'overview': {
            'total_files_analyzed': total_files,
            'total_sections': len(MAIN_SECTIONS),
            'total_functions_needed': 0,
            'total_helper_functions': set()
        },
        'section_summaries': {},
        'implementation_roadmap': []
    }

    # Process each section
    for section_key, analysis in section_analyses.items():
        coverage = len(analysis['countries_with_section']) / total_files * 100

        section_summary = {
            'display_name': analysis['section_display_name'],
            'coverage_percentage': coverage,
            'total_properties': analysis['total_properties'],
            'helper_functions_needed': list(analysis['helper_functions_needed'])
        }

        master_summary['section_summaries'][section_key] = section_summary
        master_summary['overview']['total_functions_needed'] += analysis['total_properties']
        master_summary['overview']['total_helper_functions'].update(
            analysis['helper_functions_needed'])

        # Add to implementation roadmap
        master_summary['implementation_roadmap'].append({
            'section_key': section_key,
            'display_name': analysis['section_display_name'],
            'priority_score': coverage * analysis['total_properties'],
            'coverage_percentage': coverage,
            'complexity': len(analysis['helper_functions_needed'])
        })

    # Sort roadmap by priority
    master_summary['implementation_roadmap'].sort(
        key=lambda x: x['priority_score'], reverse=True)
    master_summary['overview']['total_helper_functions'] = list(
        master_summary['overview']['total_helper_functions'])

    # Save master summary
    with open(os.path.join(utils_folder, 'cia_master_summary.json'), 'w', encoding='utf-8') as f:
        json.dump(master_summary, f, indent=2, ensure_ascii=False)

    print(
        f"Analysis complete! Generated reports for {len(section_analyses)} sections.")
    print(
        f"Total functions needed: {master_summary['overview']['total_functions_needed']}")
    print(
        f"Total helper functions: {len(master_summary['overview']['total_helper_functions'])}")


def convert_sets_to_lists(obj):
    """
    Recursively convert sets to lists for JSON serialization
    """
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, dict):
        return {k: convert_sets_to_lists(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets_to_lists(item) for item in obj]
    else:
        return obj


######################################################################################################################
#   MAIN EXECUTION
######################################################################################################################
if __name__ == '__main__':
    print("Starting focused CIA section analysis...")
    results = analyze_cia_sections_focused()
    print("Analysis complete! Check the generated section reports.")
