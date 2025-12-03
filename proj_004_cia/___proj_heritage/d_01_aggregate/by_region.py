"""
Aggregate sites by UNESCO region.
"""

from typing import Dict, List
from collections import defaultdict
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.config import REGIONS


def aggregate_by_region(normalized_sites: List[Dict]) -> Dict[str, Dict]:
    """
    Group sites by UNESCO region.

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with region codes as keys

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> by_region = aggregate_by_region(sites)
        >>> by_region['EUR']['total_sites']
        580
    """
    app_logger.info("Aggregating sites by region...")

    region_data = defaultdict(lambda: {
        'region_code': None,
        'region_name': None,
        'total_sites': 0,
        'sites_by_category': {'Cultural': 0, 'Natural': 0, 'Mixed': 0},
        'transboundary_sites': 0,
        'endangered_sites': 0,
        'countries': set(),
        'sites': []
    })

    # Group sites by region
    for site in normalized_sites:
        region_code = site['geography']['region']['code']
        region_name = site['geography']['region']['name']
        category = site['classification']['category']['name']
        is_transboundary = site['geography']['is_transboundary']
        is_endangered = site['temporal']['danger_status']['is_endangered']
        countries = site['geography']['countries'].keys()

        # Initialize region data
        if region_data[region_code]['region_code'] is None:
            region_data[region_code]['region_code'] = region_code
            region_data[region_code]['region_name'] = region_name

        # Add site
        region_data[region_code]['sites'].append(site['site_key'])
        region_data[region_code]['total_sites'] += 1

        # Update category counts
        region_data[region_code]['sites_by_category'][category] += 1

        # Update countries in region
        region_data[region_code]['countries'].update(countries)

        # Update flags
        if is_transboundary:
            region_data[region_code]['transboundary_sites'] += 1

        if is_endangered:
            region_data[region_code]['endangered_sites'] += 1

    # Convert sets to lists and sort
    result = {}
    for code, data in region_data.items():
        data['countries'] = sorted(list(data['countries']))
        data['country_count'] = len(data['countries'])
        result[code] = data

    # Sort by site count
    result = dict(sorted(
        result.items(),
        key=lambda x: x[1]['total_sites'],
        reverse=True
    ))

    app_logger.success(f"✓ Aggregated {len(result)} regions")

    return result


def get_region_stats(region_data: Dict) -> Dict:
    """
    Get statistics about region aggregation.

    Args:
        region_data: Output from aggregate_by_region()

    Returns:
        Dictionary with statistics
    """
    stats = {
        'total_regions': len(region_data),
        'regions_summary': [],
    }

    for code, data in region_data.items():
        stats['regions_summary'].append({
            'code': code,
            'name': data['region_name'],
            'sites': data['total_sites'],
            'countries': data['country_count']
        })

    return stats
