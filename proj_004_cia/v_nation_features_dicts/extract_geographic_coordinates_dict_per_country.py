"""
Extract geographic coordinates dictionary for each country.

Returns latitude and longitude coordinates for each nation.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract geographic coordinates from parsed geography data."""
    return parsed_data.get('geographic_coordinates', {})


def get_geographic_coordinates(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract geographic coordinates for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and coordinate dicts as values
        Example: {'USA': {'coordinates': {'latitude': 38.0, 'longitude': -97.0}}}
    """
    return extract_dict_feature(
        parser_func=return_geography_data,
        extractor_func=_extract_from_parsed,
        feature_name="geographic_coordinates",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_geographic_coordinates(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
    print("\nSample output (JPN):")
    pprint(data.get('JPN', {}))
