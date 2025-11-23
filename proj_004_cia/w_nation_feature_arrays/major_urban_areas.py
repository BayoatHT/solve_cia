"""
Extract Major Urban Areas Array

Returns a dictionary with ISO3 codes as keys and arrays of city dicts as values.
Each city dict contains: city, population
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_major_urban_areas(parsed_data: dict) -> list:
    """Extract major urban areas array from parsed society data."""
    mua = parsed_data.get('major_urban_areas', {})
    return mua.get('major_urban_areas', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_society_data,
        extractor_func=extract_major_urban_areas,
        feature_name="major_urban_areas"
    )
