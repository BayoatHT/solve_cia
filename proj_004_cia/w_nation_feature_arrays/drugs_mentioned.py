"""
Extract Drugs Mentioned Array

Returns a dictionary with ISO3 codes as keys and arrays of mentioned drugs as values.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from proj_004_cia.c_13_issues.return_issues_data import return_issues_data
from proj_004_cia.w_nation_feature_arrays.base_extractor import run_extraction


def extract_drugs_mentioned(parsed_data: dict) -> list:
    """Extract drugs mentioned array from parsed issues data."""
    drugs = parsed_data.get('illicit_drugs', {})
    return drugs.get('drugs_mentioned', [])


if __name__ == "__main__":
    data = run_extraction(
        parser_func=return_issues_data,
        extractor_func=extract_drugs_mentioned,
        feature_name="drugs_mentioned"
    )
