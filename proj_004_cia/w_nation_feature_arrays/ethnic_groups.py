"""
Extract Ethnic Groups Array

Returns a dictionary with ISO3 codes as keys and arrays of ethnic group dicts as values.
Each ethnic group dict contains: name, percentage (where available)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_ethnic_groups(parsed_data: dict) -> list:
    """Extract ethnic groups array from parsed society data."""
    eg = parsed_data.get('ethnic_groups', {})
    return eg.get('ethnic_groups', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_society_data,
        extractor_func=extract_ethnic_groups,
        feature_name="ethnic_groups"
    )
