######################################################################################################################
#   ENHANCED CIA JSON MAPPING SYSTEM
# ---------------------------------------------------------------------------------------------------------------------
import os
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple
# ---------------------------------------------------------------------------------------------------------------------

######################################################################################################################
#   ENHANCED MAPPING FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------


def analyze_json_structure_comprehensive():
    """
    Comprehensive analysis of CIA JSON structure including:
    - Key hierarchy mapping
    - Data type analysis
    - Value pattern recognition
    - Complexity assessment
    - Missing data patterns
    """

    # ESTABLISH PATHS
    analysis_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\a_05_parsing_report\analysis_folder'
    raw_data_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\_raw_data'

    # ANALYSIS CONTAINERS
    analysis_results = {
        'key_hierarchy': defaultdict(set),
        'data_types': defaultdict(Counter),
        'value_patterns': defaultdict(set),
        'complexity_metrics': defaultdict(dict),
        'missing_data': defaultdict(int),
        'sample_values': defaultdict(list),
        'parsing_challenge_counts': defaultdict(Counter),  # Changed to Counter
        'countries_with_key': defaultdict(set),
        'key_statistics': {}
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

                # Analyze this file's structure
                analyze_file_structure(data, analysis_results, country_code)
                total_files += 1

            except Exception as e:
                print(f"Error processing {file}: {e}")

    # GENERATE COMPREHENSIVE STATISTICS
    analysis_results['key_statistics'] = generate_key_statistics(
        analysis_results, total_files)

    # SAVE RESULTS
    save_analysis_results(analysis_results, analysis_folder)

    return analysis_results


def analyze_file_structure(data: Dict, analysis_results: Dict, country_code: str, parent_key: str = ''):
    """
    Recursively analyze the structure of a single JSON file
    """
    if isinstance(data, dict):
        for key, value in data.items():
            full_key = f'{parent_key}.{key}' if parent_key else key

            # Track key hierarchy
            analysis_results['key_hierarchy'][parent_key].add(key)
            analysis_results['countries_with_key'][full_key].add(country_code)

            # Analyze the value
            analyze_value(value, full_key, analysis_results, country_code)

            # Recurse into nested structures
            if isinstance(value, dict):
                analyze_file_structure(
                    value, analysis_results, country_code, full_key)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                for item in value:
                    analyze_file_structure(
                        item, analysis_results, country_code, full_key)


def analyze_value(value: Any, key: str, analysis_results: Dict, country_code: str):
    """
    Analyze individual values for type, patterns, and complexity
    """
    # Track data types
    value_type = type(value).__name__
    analysis_results['data_types'][key][value_type] += 1

    # Handle None/null values
    if value is None:
        analysis_results['missing_data'][key] += 1
        return

    # Store sample values (limit to avoid memory issues)
    if len(analysis_results['sample_values'][key]) < 5:
        analysis_results['sample_values'][key].append(value)

    # Analyze based on type
    if isinstance(value, str):
        analyze_string_value(value, key, analysis_results)
    elif isinstance(value, (int, float)):
        analyze_numeric_value(value, key, analysis_results)
    elif isinstance(value, dict):
        analyze_dict_complexity(value, key, analysis_results)
    elif isinstance(value, list):
        analyze_list_complexity(value, key, analysis_results)


def analyze_string_value(value: str, key: str, analysis_results: Dict):
    """
    Analyze string values for patterns and parsing challenges
    """
    # Pattern recognition
    patterns = {
        'html_content': bool(re.search(r'<[^>]+>', value)),
        'percentage': bool(re.search(r'\d+\.?\d*%', value)),
        'currency': bool(re.search(r'[\$€£¥]|\d+\.\d+\s*(million|billion|trillion)', value)),
        'date_range': bool(re.search(r'\d{4}-\d{4}|\d{1,2}/\d{1,2}/\d{4}', value)),
        'numeric_range': bool(re.search(r'\d+\.?\d*\s*-\s*\d+\.?\d*', value)),
        'coordinates': bool(re.search(r'\d+\s*\d+\s*[NS],?\s*\d+\s*\d+\s*[EW]', value)),
        'multi_line': '\n' in value or len(value) > 200,
        'contains_numbers': bool(re.search(r'\d', value)),
        'mixed_languages': bool(re.search(r'[^\x00-\x7F]', value)),
        'list_format': bool(re.search(r'[;,]\s*\w+', value))
    }

    for pattern_name, found in patterns.items():
        if found:
            analysis_results['value_patterns'][key].add(pattern_name)

    # Identify parsing challenges - use Counter to track frequency
    if 'parsing_challenge_counts' not in analysis_results:
        analysis_results['parsing_challenge_counts'] = defaultdict(Counter)

    if patterns['html_content']:
        analysis_results['parsing_challenge_counts'][key]['HTML_PARSING'] += 1
    if patterns['numeric_range']:
        analysis_results['parsing_challenge_counts'][key]['RANGE_EXTRACTION'] += 1
    if patterns['currency']:
        analysis_results['parsing_challenge_counts'][key]['CURRENCY_NORMALIZATION'] += 1
    if patterns['date_range']:
        analysis_results['parsing_challenge_counts'][key]['DATE_PARSING'] += 1
    if patterns['list_format']:
        analysis_results['parsing_challenge_counts'][key]['LIST_SPLITTING'] += 1
    if patterns['coordinates']:
        analysis_results['parsing_challenge_counts'][key]['COORDINATE_PARSING'] += 1


def analyze_numeric_value(value: float, key: str, analysis_results: Dict):
    """
    Analyze numeric values for ranges and patterns
    """
    # Track numeric patterns
    if isinstance(value, int):
        analysis_results['value_patterns'][key].add('integer')
    else:
        analysis_results['value_patterns'][key].add('decimal')

    # Check for special numeric patterns
    if value == 0:
        analysis_results['value_patterns'][key].add('zero_value')
    elif value < 0:
        analysis_results['value_patterns'][key].add('negative_value')
    elif value > 1000000:
        analysis_results['value_patterns'][key].add('large_number')


def analyze_dict_complexity(value: Dict, key: str, analysis_results: Dict):
    """
    Analyze dictionary complexity
    """
    complexity_metrics = {
        'nested_levels': calculate_nesting_depth(value),
        'total_keys': count_all_keys(value),
        'max_keys_per_level': max_keys_per_level(value)
    }

    analysis_results['complexity_metrics'][key] = complexity_metrics

    # Use Counter for parsing challenges
    if 'parsing_challenge_counts' not in analysis_results:
        analysis_results['parsing_challenge_counts'] = defaultdict(Counter)

    if complexity_metrics['nested_levels'] > 3:
        analysis_results['parsing_challenge_counts'][key]['DEEP_NESTING'] += 1


def analyze_list_complexity(value: List, key: str, analysis_results: Dict):
    """
    Analyze list complexity and contents
    """
    if not value:
        analysis_results['value_patterns'][key].add('empty_list')
        return

    # Analyze list contents
    item_types = set(type(item).__name__ for item in value)
    analysis_results['value_patterns'][key].add(
        f'list_of_{",".join(item_types)}')

    # Use Counter for parsing challenges
    if 'parsing_challenge_counts' not in analysis_results:
        analysis_results['parsing_challenge_counts'] = defaultdict(Counter)

    if len(item_types) > 1:
        analysis_results['parsing_challenge_counts'][key]['MIXED_TYPE_LIST'] += 1


def calculate_nesting_depth(obj: Any, current_depth: int = 0) -> int:
    """
    Calculate the maximum nesting depth of a nested structure
    """
    if isinstance(obj, dict):
        if not obj:
            return current_depth
        return max(calculate_nesting_depth(v, current_depth + 1) for v in obj.values())
    elif isinstance(obj, list):
        if not obj:
            return current_depth
        return max(calculate_nesting_depth(item, current_depth + 1) for item in obj)
    else:
        return current_depth


def count_all_keys(obj: Dict) -> int:
    """
    Count total number of keys in nested dictionary
    """
    count = len(obj)
    for value in obj.values():
        if isinstance(value, dict):
            count += count_all_keys(value)
    return count


def max_keys_per_level(obj: Dict) -> int:
    """
    Find maximum number of keys at any single level
    """
    max_keys = len(obj)
    for value in obj.values():
        if isinstance(value, dict):
            max_keys = max(max_keys, max_keys_per_level(value))
    return max_keys


def generate_key_statistics(analysis_results: Dict, total_files: int) -> Dict:
    """
    Generate comprehensive statistics about the keys
    """
    statistics = {
        'total_files_analyzed': total_files,
        'unique_keys': len(analysis_results['countries_with_key']),
        'key_coverage': {},
        'most_common_patterns': {},
        'parsing_complexity': {},
        'data_quality_issues': {}
    }

    # Calculate key coverage (what percentage of countries have each key)
    for key, countries in analysis_results['countries_with_key'].items():
        coverage_percent = (len(countries) / total_files) * 100
        statistics['key_coverage'][key] = {
            'coverage_percent': coverage_percent,
            'countries_count': len(countries),
            'missing_from': total_files - len(countries)
        }

    # Most common patterns
    for key, patterns in analysis_results['value_patterns'].items():
        statistics['most_common_patterns'][key] = list(patterns)

    # Parsing complexity assessment
    for key, challenge_counts in analysis_results['parsing_challenge_counts'].items():
        if challenge_counts:
            statistics['parsing_complexity'][key] = {
                # Convert Counter to dict with counts
                'challenge_types': dict(challenge_counts),
                # Number of unique challenge types
                'complexity_score': len(challenge_counts),
                # Total occurrences
                'total_challenges': sum(challenge_counts.values())
            }

    # Data quality issues
    for key, missing_count in analysis_results['missing_data'].items():
        if missing_count > 0:
            statistics['data_quality_issues'][key] = {
                'missing_count': missing_count,
                'missing_percent': (missing_count / total_files) * 100
            }

    return statistics


def save_analysis_results(analysis_results: Dict, analysis_folder: str):
    """
    Save the comprehensive analysis results to multiple files
    """
    utils_folder = analysis_folder
    os.makedirs(utils_folder, exist_ok=True)

    # Convert sets to lists for JSON serialization
    serializable_results = {}
    for key, value in analysis_results.items():
        if isinstance(value, defaultdict):
            serializable_results[key] = dict(value)
        else:
            serializable_results[key] = value

    # Convert sets to lists in nested structures
    for key in ['key_hierarchy', 'value_patterns', 'countries_with_key']:
        if key in serializable_results:
            serializable_results[key] = {
                k: list(v) if isinstance(v, set) else v
                for k, v in serializable_results[key].items()
            }

    # Save comprehensive analysis
    with open(os.path.join(utils_folder, 'cia_comprehensive_analysis.json'), 'w', encoding='utf-8') as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)

    # Save parsing priority list
    parsing_priority = generate_parsing_priority(analysis_results)
    with open(os.path.join(utils_folder, 'cia_parsing_priority.json'), 'w', encoding='utf-8') as f:
        json.dump(parsing_priority, f, indent=2, ensure_ascii=False)

    # Save function requirements
    function_requirements = generate_function_requirements(analysis_results)
    with open(os.path.join(utils_folder, 'cia_function_requirements.json'), 'w', encoding='utf-8') as f:
        json.dump(function_requirements, f, indent=2, ensure_ascii=False)

    print(f"Comprehensive analysis saved to {utils_folder}")


def generate_parsing_priority(analysis_results: Dict) -> List[Dict]:
    """
    Generate a priority list for parsing functions based on complexity and coverage
    """
    priority_list = []

    for key, countries in analysis_results['countries_with_key'].items():
        coverage = len(countries)
        complexity_score = 0

        # Calculate complexity score
        if key in analysis_results['parsing_challenge_counts']:
            complexity_score += len(
                analysis_results['parsing_challenge_counts'][key])

        if key in analysis_results['complexity_metrics']:
            complexity_score += analysis_results['complexity_metrics'][key].get(
                'nested_levels', 0)

        # Get challenge details with counts
        challenge_details = {}
        if key in analysis_results['parsing_challenge_counts']:
            challenge_details = dict(
                analysis_results['parsing_challenge_counts'][key])

        priority_list.append({
            'key': key,
            # High coverage, low complexity = high priority
            'priority_score': coverage * 10 - complexity_score,
            'coverage': coverage,
            'complexity_score': complexity_score,
            'challenge_details': challenge_details,  # Dict with counts instead of list
            'patterns': list(analysis_results['value_patterns'].get(key, []))
        })

    return sorted(priority_list, key=lambda x: x['priority_score'], reverse=True)


def generate_function_requirements(analysis_results: Dict) -> Dict:
    """
    Generate specific requirements for each parsing function
    """
    requirements = {}

    for key in analysis_results['countries_with_key'].keys():
        # Get challenge details with counts
        challenge_details = {}
        if key in analysis_results['parsing_challenge_counts']:
            challenge_details = dict(
                analysis_results['parsing_challenge_counts'][key])

        requirements[key] = {
            'function_name': f"parse_{key.replace('.', '_').replace(' ', '_').lower()}",
            'input_types': list(analysis_results['data_types'].get(key, {}).keys()),
            'output_requirements': [],
            'challenge_details': challenge_details,  # Dict with counts
            'sample_values': analysis_results['sample_values'].get(key, [])[:3],
            'coverage_percent': (len(analysis_results['countries_with_key'][key]) /
                                 analysis_results['key_statistics']['total_files_analyzed']) * 100,
            'complexity_metrics': analysis_results['complexity_metrics'].get(key, {}),
            'value_patterns': list(analysis_results['value_patterns'].get(key, []))
        }

        # Generate output requirements based on patterns
        patterns = analysis_results['value_patterns'].get(key, [])
        if 'percentage' in patterns:
            requirements[key]['output_requirements'].append(
                'normalize_percentage_to_float')
        if 'currency' in patterns:
            requirements[key]['output_requirements'].append(
                'normalize_currency_to_usd')
        if 'date_range' in patterns:
            requirements[key]['output_requirements'].append(
                'parse_date_range_to_dict')
        if 'numeric_range' in patterns:
            requirements[key]['output_requirements'].append(
                'split_range_to_min_max')
        if 'coordinates' in patterns:
            requirements[key]['output_requirements'].append(
                'parse_coordinates_to_decimal')

    return requirements

######################################################################################################################
#   ENHANCED REPORTING FUNCTIONS
######################################################################################################################


def generate_parsing_report(analysis_results: Dict) -> str:
    """
    Generate a comprehensive text report of parsing requirements
    """
    report = []
    report.append("=" * 80)
    report.append("CIA JSON PARSING REQUIREMENTS REPORT")
    report.append("=" * 80)

    stats = analysis_results['key_statistics']
    report.append(f"Total Files Analyzed: {stats['total_files_analyzed']}")
    report.append(f"Unique Keys Found: {stats['unique_keys']}")
    report.append("")

    # High priority functions
    report.append("HIGH PRIORITY PARSING FUNCTIONS:")
    report.append("-" * 40)
    high_priority = [k for k, v in stats['key_coverage'].items()
                     if v['coverage_percent'] > 80]
    for key in high_priority[:10]:
        coverage = stats['key_coverage'][key]['coverage_percent']
        challenges = stats['parsing_complexity'].get(
            key, {}).get('challenge_types', {})
        challenge_summary = ', '.join(
            [f"{k}({v})" for k, v in challenges.items()]) if challenges else "None"
        report.append(
            f"  {key}: {coverage:.1f}% coverage, Challenges: {challenge_summary}")

    report.append("")
    report.append("COMPLEX PARSING CHALLENGES:")
    report.append("-" * 40)
    complex_keys = sorted(stats['parsing_complexity'].items(),
                          key=lambda x: x[1]['complexity_score'], reverse=True)
    for key, complexity in complex_keys[:10]:
        challenge_details = ', '.join(
            [f"{k}({v})" for k, v in complexity['challenge_types'].items()])
        total_challenges = complexity.get('total_challenges', 0)
        report.append(
            f"  {key}: Score {complexity['complexity_score']}, Total: {total_challenges}, Details: {challenge_details}")

    report.append("")
    report.append("DATA QUALITY ISSUES:")
    report.append("-" * 40)
    for key, issues in stats['data_quality_issues'].items():
        if issues['missing_percent'] > 20:
            report.append(
                f"  {key}: {issues['missing_percent']:.1f}% missing data")

    return "\n".join(report)

######################################################################################################################
#   MAIN EXECUTION
######################################################################################################################


if __name__ == '__main__':
    print("Starting comprehensive CIA JSON analysis...")
    results = analyze_json_structure_comprehensive()

    # Generate and save report
    report = generate_parsing_report(results)
    print("\n" + report)
    utils_folder = r'C:\Users\bayoa\impact_projects\claude_solve_cia\proj_004_cia\a_05_parsing_report\analysis_folder'
    with open(os.path.join(utils_folder, 'cia_parsing_report.txt'), 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nAnalysis complete! Check the generated files in: {utils_folder}")
