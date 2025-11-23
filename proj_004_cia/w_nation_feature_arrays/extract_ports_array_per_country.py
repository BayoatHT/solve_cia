"""
Extract Ports Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of ports as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_ports_array_per_country import get_ports
    data = get_ports()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_09_transportation.return_transportation_data import return_transportation_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract ports array from parsed data."""
    return parsed_data.get('ports', {}).get('ports_key_list', [])


def get_ports(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get ports for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of ports as values
    """
    return extract_feature(
        parser_func=return_transportation_data,
        extractor_func=_extract_from_parsed,
        feature_name="ports",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_ports(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
