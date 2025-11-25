"""
Extract phone_fixed_lines dictionary for each country.

Returns phone_fixed_lines data from Communications category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_08_communications.return_communications_data import return_communications_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract phone_fixed_lines from parsed communications data."""
    return parsed_data.get('phone_fixed_lines', {})


def get_phone_fixed_lines(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract phone_fixed_lines data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and phone_fixed_lines dicts as values
    """
    return extract_dict_feature(
        parser_func=return_communications_data,
        extractor_func=_extract_from_parsed,
        feature_name="phone_fixed_lines",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_phone_fixed_lines(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
