"""
Extract broadband_fixed dictionary for each country.

Returns broadband_fixed data from Communications category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_08_communications.return_communications_data import return_communications_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract broadband_fixed from parsed communications data."""
    return parsed_data.get('broadband_fixed', {})


def get_broadband_fixed(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract broadband_fixed data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and broadband_fixed dicts as values
    """
    return extract_dict_feature(
        parser_func=return_communications_data,
        extractor_func=_extract_from_parsed,
        feature_name="broadband_fixed",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_broadband_fixed(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
