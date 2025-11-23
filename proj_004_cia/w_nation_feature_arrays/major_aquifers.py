"""
Extract Major Aquifers Array

Returns a dictionary with ISO3 codes as keys and arrays of aquifer names as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_major_aquifers(parsed_data: dict) -> list:
    """Extract major aquifers array from parsed environment data."""
    ma = parsed_data.get('major_aquifers', {})
    return ma.get('major_aquifers', {}).get('aquifers', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_environment_data,
        extractor_func=extract_major_aquifers,
        feature_name="major_aquifers"
    )
