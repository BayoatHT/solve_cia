"""
Extract Agricultural Products Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of agricultural products as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_agricultural_products_array_per_country import get_agricultural_products
    data = get_agricultural_products()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract agricultural products array from parsed economy data."""
    ag = parsed_data.get('agricultural_products', {})
    return ag.get('agricultural_products', [])


def get_agricultural_products(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get agricultural products for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and arrays of agricultural products as values

    Example:
        >>> data = get_agricultural_products()
        >>> data['USA']
        ['maize', 'soybeans', 'milk', 'wheat', ...]
    """
    return extract_feature(
        parser_func=return_economy_data,
        extractor_func=_extract_from_parsed,
        feature_name="agricultural_products",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_agricultural_products(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
