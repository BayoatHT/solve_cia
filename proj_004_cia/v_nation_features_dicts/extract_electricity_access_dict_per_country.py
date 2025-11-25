"""
Extract electricity_access dictionary for each country.

Returns electricity_access data from Energy category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_07_energy.return_energy_data import return_energy_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract electricity_access from parsed energy data."""
    return parsed_data.get('electricity_access', {})


def get_electricity_access(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract electricity_access data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and electricity_access dicts as values
    """
    return extract_dict_feature(
        parser_func=return_energy_data,
        extractor_func=_extract_from_parsed,
        feature_name="electricity_access",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_electricity_access(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
