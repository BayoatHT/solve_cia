"""
Extract carbon_dioxide_emissions dictionary for each country.

Returns carbon_dioxide_emissions data from Energy category.
"""

import os
import sys
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_07_energy.return_energy_data import return_energy_data
from proj_004_cia.v_nation_features_dicts.base_extractor import extract_dict_feature


def _extract_from_parsed(parsed_data: dict) -> dict:
    """Extract carbon_dioxide_emissions from parsed energy data."""
    return parsed_data.get('carbon_dioxide_emissions', {})


def get_carbon_dioxide_emissions(verbose: bool = False) -> Dict[str, Dict]:
    """
    Extract carbon_dioxide_emissions data for all countries.

    Args:
        verbose: If True, print progress

    Returns:
        Dictionary with ISO3 codes as keys and carbon_dioxide_emissions dicts as values
    """
    return extract_dict_feature(
        parser_func=return_energy_data,
        extractor_func=_extract_from_parsed,
        feature_name="carbon_dioxide_emissions",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_carbon_dioxide_emissions(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', {}))
