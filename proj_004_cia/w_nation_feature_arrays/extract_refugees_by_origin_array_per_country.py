"""
Extract Refugees By Origin Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of refugees_by_origin as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_refugees_by_origin_array_per_country import get_refugees_by_origin
    data = get_refugees_by_origin()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_13_issues.return_issues_data import return_issues_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract refugees_by_origin array from parsed data."""
    return parsed_data.get('displaced_persons', {}).get('refugees_by_origin', [])


def get_refugees_by_origin(verbose: bool = False) -> Dict[str, List[dict]]:
    """
    Get refugees_by_origin for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of refugees_by_origin as values
    """
    return extract_feature(
        parser_func=return_issues_data,
        extractor_func=_extract_from_parsed,
        feature_name="refugees_by_origin",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_refugees_by_origin(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
