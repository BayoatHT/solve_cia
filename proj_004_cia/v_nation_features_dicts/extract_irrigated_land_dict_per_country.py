"""
Extract irrigated_land dictionary for each country.

Returns irrigated_land data from Geography category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract irrigated_land from parsed geography data."""
    return parsed_data.get('irrigated_land', {})


def get_irrigated_land(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract irrigated_land data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and irrigated_land dicts as values
    """
    return extract_dict_feature(
        parser_func=return_geography_data,
        extractor_func=_extract_from_parsed,
        feature_name="irrigated_land",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_irrigated_land(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
