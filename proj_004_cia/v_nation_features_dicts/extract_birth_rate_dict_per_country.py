"""
Extract birth_rate dictionary for each country.

Returns birth_rate data from Society category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract birth_rate from parsed society data."""
    return parsed_data.get('birth_rate', {})


def get_birth_rate(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract birth_rate data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and birth_rate dicts as values
    """
    return extract_dict_feature(
        parser_func=return_society_data,
        extractor_func=_extract_from_parsed,
        feature_name="birth_rate",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_birth_rate(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
