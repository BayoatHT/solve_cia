"""
Extract Religions Array

Returns a dictionary with ISO3 codes as keys and arrays of religion dicts as values.
Each religion dict contains: name, percentage (where available)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_religions(parsed_data: dict) -> list:
    """Extract religions array from parsed society data."""
    rel = parsed_data.get('religions', {})
    return rel.get('religions', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_society_data,
        extractor_func=extract_religions,
        feature_name="religions"
    )
