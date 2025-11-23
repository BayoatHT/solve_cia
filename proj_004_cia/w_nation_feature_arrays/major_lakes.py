"""
Extract Major Lakes Array

Returns a dictionary with ISO3 codes as keys and arrays of lake dicts as values.
Each lake dict contains: name, area_sq_km (or area_sq_km_min/max for ranges), shared_with (optional)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_major_lakes(parsed_data: dict) -> list:
    """Extract major lakes array from parsed environment data."""
    ml = parsed_data.get('major_lakes', {})
    lakes_data = ml.get('major_lakes', {})
    # Combine fresh and salt water lakes
    fresh = lakes_data.get('fresh_water', [])
    salt = lakes_data.get('salt_water', [])
    return fresh + salt


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_environment_data,
        extractor_func=extract_major_lakes,
        feature_name="major_lakes"
    )
