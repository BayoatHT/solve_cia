"""
Extract railways dictionary for each country.

Returns railways data from Transportation category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_09_transportation.return_transportation_data import return_transportation_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract railways from parsed transportation data."""
    return parsed_data.get('railways', {})


def get_railways(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract railways data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and railways dicts as values
    """
    return extract_dict_feature(
        parser_func=return_transportation_data,
        extractor_func=_extract_from_parsed,
        feature_name="railways",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_railways(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
