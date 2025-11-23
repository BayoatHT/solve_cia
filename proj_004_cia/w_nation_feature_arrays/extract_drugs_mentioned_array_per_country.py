"""
Extract Drugs Mentioned Array Per Country

Returns a dictionary with ISO3 codes as keys and arrays of drugs_mentioned as values.

Usage:
    from proj_004_cia.w_nation_feature_arrays.extract_drugs_mentioned_array_per_country import get_drugs_mentioned
    data = get_drugs_mentioned()
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from proj_004_cia.c_13_issues.return_issues_data import return_issues_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import extract_feature


def _extract_from_parsed(parsed_data: dict) -> list:
    """Extract drugs_mentioned array from parsed data."""
    return parsed_data.get('illicit_drugs', {}).get('drugs_mentioned', [])


def get_drugs_mentioned(verbose: bool = False) -> Dict[str, List[str]]:
    """
    Get drugs_mentioned for all countries.

    Returns:
        Dictionary with ISO3 codes as keys and arrays of drugs_mentioned as values
    """
    return extract_feature(
        parser_func=return_issues_data,
        extractor_func=_extract_from_parsed,
        feature_name="drugs_mentioned",
        verbose=verbose
    )


if __name__ == "__main__":
    from pprint import pprint
    data = get_drugs_mentioned(verbose=True)
    print("\nSample output (USA):")
    pprint(data.get('USA', []))
