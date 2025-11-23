"""
Extract Refugees by Origin Array

Returns a dictionary with ISO3 codes as keys and arrays of refugee origin dicts as values.
Each origin dict contains: country, count
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_13_issues.return_issues_data import return_issues_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_refugees_by_origin(parsed_data: dict) -> list:
    """Extract refugees by origin array from parsed issues data."""
    dp = parsed_data.get('displaced_persons', {})
    return dp.get('refugees_by_origin', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_issues_data,
        extractor_func=extract_refugees_by_origin,
        feature_name="refugees_by_origin"
    )
