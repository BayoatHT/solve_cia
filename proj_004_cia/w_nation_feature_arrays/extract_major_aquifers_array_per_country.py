"""
Extract Major Aquifers Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of major_aquifers as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_major_aquifers_array_per_country import get_major_aquifers
    data = get_major_aquifers()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract major_aquifers array from parsed data."""
    return parsed_data.get('major_aquifers', {}).get('major_aquifers', {}).get('aquifers', [])


def get_major_aquifers(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get major_aquifers for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of major_aquifers as values
    """
    return extract_feature(
        parser_func=return_environment_data,
        extractor_func=_extract_from_parsed,
        feature_name="major_aquifers",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_major_aquifers(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
