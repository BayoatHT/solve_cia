"""
Extract Natural Hazards Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of natural_hazards as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_natural_hazards_array_per_country import get_natural_hazards
    data = get_natural_hazards()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract natural_hazards array from parsed data."""
    return parsed_data.get('natural_hazards', {}).get('general_hazards', [])


def get_natural_hazards(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get natural_hazards for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of natural_hazards as values
    """
    return extract_feature(
        parser_func=return_geography_data,
        extractor_func=_extract_from_parsed,
        feature_name="natural_hazards",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_natural_hazards(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
