"""
Extract Natural Hazards Array

Returns a dictionary with ISO3 codes as keys and arrays of natural hazards as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_natural_hazards(parsed_data: dict) -> list:
    """Extract natural hazards array from parsed geography data."""
    nh = parsed_data.get('natural_hazards', {})
    return nh.get('general_hazards', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_geography_data,
        extractor_func=extract_natural_hazards,
        feature_name="natural_hazards"
    )
