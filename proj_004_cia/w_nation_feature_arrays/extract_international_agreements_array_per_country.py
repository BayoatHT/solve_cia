"""
Extract International Agreements Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of international_agreements as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_international_agreements_array_per_country import get_international_agreements
    data = get_international_agreements()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract international_agreements array from parsed data."""
    return parsed_data.get('env_international_agreements', {}).get('international_agreements', {}).get('party_to', [])


def get_international_agreements(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get international_agreements for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of international_agreements as values
    """
    return extract_feature(
        parser_func=return_environment_data,
        extractor_func=_extract_from_parsed,
        feature_name="international_agreements",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_international_agreements(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
