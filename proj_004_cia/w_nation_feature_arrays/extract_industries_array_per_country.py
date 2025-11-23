"""
Extract Industries Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of industries as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_industries_array_per_country import get_industries
    data = get_industries()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract industries array from parsed economy data."""
    return parsed_data.get('industries', {}).get('industries', [])


def get_industries(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get industries for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of industries as values
    """
    return extract_feature(
        parser_func=return_economy_data,
        extractor_func=_extract_from_parsed,
        feature_name="industries",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_industries(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
