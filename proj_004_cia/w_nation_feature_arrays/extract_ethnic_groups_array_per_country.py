"""
Extract Ethnic Groups Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of ethnic_groups as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_ethnic_groups_array_per_country import get_ethnic_groups
    data = get_ethnic_groups()
"""

from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature
from proj_004_cia.c_03_society.return_society_data import return_society_data
from typing import Dict, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract ethnic_groups array from parsed data."""
    return parsed_data.get('ethnic_groups', {}).get('ethnic_groups', [])


def get_ethnic_groups(verbose: bool = False) -> Dict[str, List[dict]]:
    """
    Get ethnic_groups for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of ethnic_groups as values
    """
    return extract_feature(
        parser_func=return_society_data,
        extractor_func=_extract_from_parsed,
        feature_name="ethnic_groups",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_ethnic_groups(verbose=True)
    print("\nSample output (FRA):")
    pprint(data.get('USA', []))
