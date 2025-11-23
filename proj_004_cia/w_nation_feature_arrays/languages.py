"""
Extract Languages Array

Returns a dictionary with ISO3 codes as keys and arrays of language dicts as values.
Each language dict contains: name, percentage (where available)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_languages(parsed_data: dict) -> list:
    """Extract languages array from parsed society data."""
    lang = parsed_data.get('languages', {})
    return lang.get('languages', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_society_data,
        extractor_func=extract_languages,
        feature_name="languages"
    )
