"""
Extract Border Countries Array

Returns a dictionary with ISO3 codes as keys and arrays of bordering country dicts as values.
Each border dict contains: country, border_length_km
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_border_countries(parsed_data: dict) -> list:
    """Extract border countries array from parsed geography data."""
    lb = parsed_data.get('land_boundaries', {})
    return lb.get('border_countries', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_geography_data,
        extractor_func=extract_border_countries,
        feature_name="border_countries"
    )
