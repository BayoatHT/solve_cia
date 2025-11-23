"""
Extract Environmental Issues Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of environmental_issues as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_environmental_issues_array_per_country import get_environmental_issues
    data = get_environmental_issues()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract environmental_issues array from parsed data."""
    return parsed_data.get('env_current_issues', {}).get('env_current_issues', {}).get('issues_list', [])


def get_environmental_issues(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get environmental_issues for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of environmental_issues as values
    """
    return extract_feature(
        parser_func=return_environment_data,
        extractor_func=_extract_from_parsed,
        feature_name="environmental_issues",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_environmental_issues(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
