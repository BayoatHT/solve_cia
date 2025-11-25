"""
Extract elevation dictionary for each country.

Returns highest point, lowest point, and mean elevation data.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract elevation from parsed geography data."""
    return parsed_data.get('elevation', {})


def get_elevation(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract elevation data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and elevation dicts as values
        Example: {'USA': {'highest_point': {...}, 'lowest_point': {...}, 'mean_elevation': {...}}}
    """
    return extract_dict_feature(
        parser_func=return_geography_data,
        extractor_func=_extract_from_parsed,
        feature_name="elevation",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_elevation(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
