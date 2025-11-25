"""
Extract geo_area_land_sq_km dictionary for each country.

Returns geo_area_land_sq_km data from Geography category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract geo_area_land_sq_km from parsed geography data."""
    return parsed_data.get('geo_area_land_sq_km', {})


def get_geo_area_land_sq_km(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract geo_area_land_sq_km data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and geo_area_land_sq_km dicts as values
    """
    return extract_dict_feature(
        parser_func=return_geography_data,
        extractor_func=_extract_from_parsed,
        feature_name="geo_area_land_sq_km",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_geo_area_land_sq_km(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
