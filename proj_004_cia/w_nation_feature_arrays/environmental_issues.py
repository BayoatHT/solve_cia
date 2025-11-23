"""
Extract Environmental Issues Array

Returns a dictionary with ISO3 codes as keys and arrays of environmental issues as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_environmental_issues(parsed_data: dict) -> list:
    """Extract environmental issues array from parsed environment data."""
    ei = parsed_data.get('env_current_issues', {})
    return ei.get('env_current_issues', {}).get('issues_list', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_environment_data,
        extractor_func=extract_environmental_issues,
        feature_name="environmental_issues"
    )
