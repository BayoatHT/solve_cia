"""
Extract Major Rivers Array

Returns a dictionary with ISO3 codes as keys and arrays of river dicts as values.
Each river dict contains: name, length_km, shared_with (optional)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_major_rivers(parsed_data: dict) -> list:
    """Extract major rivers array from parsed environment data."""
    mr = parsed_data.get('major_rivers', {})
    return mr.get('major_rivers', {}).get('rivers', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_environment_data,
        extractor_func=extract_major_rivers,
        feature_name="major_rivers"
    )
