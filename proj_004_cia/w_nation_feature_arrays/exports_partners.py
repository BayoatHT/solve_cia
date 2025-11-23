"""
Extract Exports Partners Array

Returns a dictionary with ISO3 codes as keys and arrays of export partner dicts as values.
Each partner dict contains: country, percentage
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_exports_partners(parsed_data: dict) -> list:
    """Extract exports partners array from parsed economy data."""
    exp = parsed_data.get('exports_partners', {})
    return exp.get('exports_partners', {}).get('partners', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_economy_data,
        extractor_func=extract_exports_partners,
        feature_name="exports_partners"
    )
