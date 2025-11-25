"""
Extract gini dictionary for each country.

Returns gini data from Economy category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract gini from parsed economy data."""
    return parsed_data.get('gini', {})


def get_gini(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract gini data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and gini dicts as values
    """
    return extract_dict_feature(
        parser_func=return_economy_data,
        extractor_func=_extract_from_parsed,
        feature_name="gini",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_gini(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
