"""
Base Extractor Utility

Common functions for extracting array features from parsed CIA data.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Any, Callable, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data, ISO3_TO_CIA


def to_python_format(data: Any) -> str:
    """Convert data to Python-friendly string format."""
    json_str = json.dumps(data, indent=4, ensure_ascii=False, default=str)
    json_str = json_str.replace(': null', ': None')
    json_str = json_str.replace(': true', ': True')
    json_str = json_str.replace(': false', ': False')
    return json_str


def extract_feature(
    parser_func: Callable,
    extractor_func: Callable,
    feature_name: str,
    verbose: bool = False
) -> Dict[str, List]:
    """
    Extract a feature array for all countries.

    Args:
        parser_func: Function to parse raw data (e.g., return_economy_data)
        extractor_func: Function to extract the specific array from parsed data
        feature_name: Name of the feature for logging
        verbose: If True, print progress and errors

    Returns:
        Dictionary with ISO3 codes as keys and arrays as values
    """
    results = {}
    errors = []

    for iso3Code in ISO3_TO_CIA.keys():
        try:
            raw_data = load_country_data(iso3Code)
            parsed = parser_func(raw_data, iso3Code)
            array_data = extractor_func(parsed)
            results[iso3Code] = array_data if array_data else []
        except Exception as e:
            errors.append(f"{iso3Code}: {str(e)}")
            results[iso3Code] = []

    if verbose and errors:
        print(f"Errors extracting {feature_name}: {len(errors)}")
        for err in errors[:3]:
            print(f"  - {err}")

    return results


def save_feature(
    data: Dict[str, List],
    feature_name: str,
    output_dir: str = None
) -> str:
    """
    Save extracted feature to a Python file.

    Args:
        data: Dictionary of ISO3 -> array
        feature_name: Name of the feature (used for filename)
        output_dir: Output directory (defaults to _outputs/)

    Returns:
        Path to saved file
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(__file__), "_outputs")
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{feature_name}.py"
    filepath = os.path.join(output_dir, filename)

    non_empty = sum(1 for v in data.values() if v)
    var_name = feature_name.upper()

    content = f'''"""
Nation Feature Array: {feature_name}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Countries with data: {non_empty} / {len(data)}

Each key is an ISO3 country code, each value is an array of {feature_name}.
"""

{var_name} = {to_python_format(data)}
'''

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def run_extraction(
    parser_func: Callable,
    extractor_func: Callable,
    feature_name: str,
    output_dir: str = None,
    save: bool = True,
    verbose: bool = True
) -> Dict[str, List]:
    """
    Run full extraction pipeline for a feature.

    Args:
        parser_func: Parser function (e.g., return_economy_data)
        extractor_func: Function to extract specific array from parsed data
        feature_name: Name of the feature
        output_dir: Output directory for saving (defaults to _outputs/)
        save: If True, save to file
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and arrays as values
    """
    if verbose:
        print(f"Extracting: {feature_name}")
        print("-" * 50)

    data = extract_feature(parser_func, extractor_func, feature_name, verbose=verbose)

    if verbose:
        non_empty = sum(1 for v in data.values() if v)
        print(f"Countries processed: {len(data)}")
        print(f"Countries with data: {non_empty}")

    if save:
        filepath = save_feature(data, feature_name, output_dir)
        if verbose:
            print(f"Saved to: {filepath}")

    return data
