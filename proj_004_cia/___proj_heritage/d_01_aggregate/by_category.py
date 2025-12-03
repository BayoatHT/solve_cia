"""
Aggregate sites by category (Cultural, Natural, Mixed).
"""

from typing import Dict, List
from collections import defaultdict
from proj_004_cia.__logger.logger import app_logger


def aggregate_by_category(normalized_sites: List[Dict]) -> Dict[str, Dict]:
    """
    Group sites by category.

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with categories as keys

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> by_category = aggregate_by_category(sites)
        >>> by_category['Cultural']['total_sites']
        972
    """
    app_logger.info("Aggregating sites by category...")

    category_data = {
        'Cultural': {
            'category': 'Cultural',
            'category_id': 1,
            'total_sites': 0,
            'sites': []
        },
        'Natural': {
            'category': 'Natural',
            'category_id': 2,
            'total_sites': 0,
            'sites': []
        },
        'Mixed': {
            'category': 'Mixed',
            'category_id': 3,
            'total_sites': 0,
            'sites': []
        }
    }

    # Group sites
    for site in normalized_sites:
        category = site['classification']['category']['name']

        category_data[category]['sites'].append(site['site_key'])
        category_data[category]['total_sites'] += 1

    app_logger.success(f"✓ Aggregated {len(category_data)} categories")

    return category_data
