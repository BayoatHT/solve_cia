"""
Aggregate sites by UNESCO criteria.
"""

from typing import Dict, List
from collections import defaultdict
from proj_004_cia.__logger.logger import app_logger


def aggregate_by_criteria(normalized_sites: List[Dict]) -> Dict:
    """
    Group sites by criteria met.

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with criteria data

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> by_criteria = aggregate_by_criteria(sites)
        >>> by_criteria['cultural']['c1']['count']
        92
    """
    app_logger.info("Aggregating sites by criteria...")

    criteria_data = {
        'cultural': {
            f'c{i}': {'criterion': i, 'count': 0, 'sites': []}
            for i in range(1, 7)
        },
        'natural': {
            f'n{i}': {'criterion': i, 'count': 0, 'sites': []}
            for i in range(7, 11)
        }
    }

    # Group sites by criteria
    for site in normalized_sites:
        criteria = site['classification']['criteria']

        # Cultural criteria
        for c_num in criteria['cultural']:
            key = f'c{c_num}'
            criteria_data['cultural'][key]['sites'].append(site['site_key'])
            criteria_data['cultural'][key]['count'] += 1

        # Natural criteria
        for n_num in criteria['natural']:
            key = f'n{n_num}'
            criteria_data['natural'][key]['sites'].append(site['site_key'])
            criteria_data['natural'][key]['count'] += 1

    app_logger.success("✓ Aggregated criteria")

    return criteria_data
