"""
Extract Ports Array

Returns a dictionary with ISO3 codes as keys and arrays of port names as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_09_transportation.return_transportation_data import return_transportation_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_ports(parsed_data: dict) -> list:
    """Extract ports array from parsed transportation data."""
    ports = parsed_data.get('ports', {})
    return ports.get('ports_key_list', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_transportation_data,
        extractor_func=extract_ports,
        feature_name="ports"
    )
