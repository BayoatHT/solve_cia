"""
Extract Exports Partners Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of exports_partners as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_exports_partners_array_per_country import get_exports_partners
    data = get_exports_partners()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract exports_partners array from parsed data."""
    return parsed_data.get('exports_partners', {}).get('exports_partners', {}).get('partners', [])


def get_exports_partners(verbose: bool = False) -> Dict[str, List[dict]]:
    """
    Get exports_partners for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of exports_partners as values
    """
    return extract_feature(
        parser_func=return_economy_data,
        extractor_func=_extract_from_parsed,
        feature_name="exports_partners",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_exports_partners(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
