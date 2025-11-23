"""
Extract Exports Commodities Array

Returns a dictionary with ISO3 codes as keys and arrays of export commodities as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_exports_commodities(parsed_data: dict) -> list:
    """Extract exports commodities array from parsed economy data."""
    exp = parsed_data.get('exports_commodities', {})
    return exp.get('exports_commodities', {}).get('commodities', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_economy_data,
        extractor_func=extract_exports_commodities,
        feature_name="exports_commodities"
    )
