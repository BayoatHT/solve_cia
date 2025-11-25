"""
Extract coastline dictionary for each country.

Returns coastline data from Geography category.
"""

from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract coastline from parsed geography data."""
    return parsed_data.get('coastline', {})


def get_coastline(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract coastline data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and coastline dicts as values
    """
    return extract_dict_feature(
        parser_func=return_geography_data,
        extractor_func=_extract_from_parsed,
        feature_name="coastline",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_coastline(verbose=True)
    print("\nSample output (NGA):")
    pprint(data.get('NGA', {}))
