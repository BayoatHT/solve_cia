"""
Extract Major Lakes Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of major_lakes as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_major_lakes_array_per_country import get_major_lakes
    data = get_major_lakes()
"""

from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from typing import Dict, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract major_lakes array from parsed data."""
    return parsed_data.get('major_lakes', {}).get('major_lakes', {}).get('fresh_water', []) + parsed_data.get('major_lakes', {}).get('major_lakes', {}).get('salt_water', [])


def get_major_lakes(verbose: bool = False) -> Dict[str, List[dict]]:
    """
    Get major_lakes for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of major_lakes as values
    """
    return extract_feature(
        parser_func=return_environment_data,
        extractor_func=_extract_from_parsed,
        feature_name="major_lakes",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_major_lakes(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
