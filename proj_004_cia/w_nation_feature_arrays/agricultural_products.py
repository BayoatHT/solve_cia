"""
Extract Agricultural Products Array

Returns a dictionary with ISO3 codes as keys and arrays of agricultural products as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_agricultural_products(parsed_data: dict) -> list:
    """Extract agricultural products array from parsed economy data."""
    ag = parsed_data.get('agricultural_products', {})
    return ag.get('agricultural_products', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_economy_data,
        extractor_func=extract_agricultural_products,
        feature_name="agricultural_products"
    )
