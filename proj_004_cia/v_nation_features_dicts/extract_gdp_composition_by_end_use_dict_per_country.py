"""
Extract gdp_composition_by_end_use dictionary for each country.

Returns gdp_composition_by_end_use data from Economy category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract gdp_composition_by_end_use from parsed economy data."""
    return parsed_data.get('gdp_composition_by_end_use', {})


def get_gdp_composition_by_end_use(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract gdp_composition_by_end_use data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and gdp_composition_by_end_use dicts as values
    """
    return extract_dict_feature(
        parser_func=return_economy_data,
        extractor_func=_extract_from_parsed,
        feature_name="gdp_composition_by_end_use",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_gdp_composition_by_end_use(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
