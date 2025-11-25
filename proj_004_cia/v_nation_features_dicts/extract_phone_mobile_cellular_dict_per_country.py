"""
Extract phone_mobile_cellular dictionary for each country.

Returns phone_mobile_cellular data from Communications category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_08_communications.return_communications_data import return_communications_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract phone_mobile_cellular from parsed communications data."""
    return parsed_data.get('phone_mobile_cellular', {})


def get_phone_mobile_cellular(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract phone_mobile_cellular data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and phone_mobile_cellular dicts as values
    """
    return extract_dict_feature(
        parser_func=return_communications_data,
        extractor_func=_extract_from_parsed,
        feature_name="phone_mobile_cellular",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_phone_mobile_cellular(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
