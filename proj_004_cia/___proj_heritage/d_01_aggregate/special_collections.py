"""
Create special collections of sites.
"""

from typing import Dict, List
from proj_004_cia.__logger.logger import app_logger


def create_special_collections(normalized_sites: List[Dict]) -> Dict:
    """
    Create special collections (transboundary, endangered, etc.).

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with special collection data

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> collections = create_special_collections(sites)
        >>> collections['transboundary']['count']
        51
    """
    app_logger.info("Creating special collections...")

    collections = {
        'transboundary': {
            'name': 'Transboundary World Heritage Sites',
            'description': 'Sites that span multiple countries',
            'count': 0,
            'sites': []
        },
        'endangered': {
            'name': 'Sites in Danger',
            'description': 'Sites on the UNESCO Danger List',
            'count': 0,
            'sites': []
        },
        'large_sites': {
            'name': 'Large Heritage Sites',
            'description': 'Sites over 1,000,000 hectares',
            'count': 0,
            'sites': []
        },
        'recent_inscriptions': {
            'name': 'Recent Inscriptions',
            'description': 'Sites inscribed in the last 5 years',
            'count': 0,
            'sites': []
        },
        'multi_component': {
            'name': 'Multi-Component Sites',
            'description': 'Sites with multiple locations (10+ components)',
            'count': 0,
            'sites': []
        }
    }

    # Determine recent year threshold
    from datetime import datetime
    current_year = datetime.now().year
    recent_threshold = current_year - 5

    # Categorize sites
    for site in normalized_sites:
        site_key = site['site_key']

        # Transboundary
        if site['geography']['is_transboundary']:
            collections['transboundary']['sites'].append(site_key)
            collections['transboundary']['count'] += 1

        # Endangered
        if site['temporal']['danger_status']['is_endangered']:
            collections['endangered']['sites'].append(site_key)
            collections['endangered']['count'] += 1

        # Large sites
        area = site['classification']['area']
        if area['available'] and area['hectares'] >= 1000000:
            collections['large_sites']['sites'].append(site_key)
            collections['large_sites']['count'] += 1

        # Recent inscriptions
        inscription_year = site['temporal']['inscription']['primary_date']
        if inscription_year and inscription_year >= recent_threshold:
            collections['recent_inscriptions']['sites'].append(site_key)
            collections['recent_inscriptions']['count'] += 1

        # Multi-component
        if site['components']['count'] >= 10:
            collections['multi_component']['sites'].append(site_key)
            collections['multi_component']['count'] += 1

    app_logger.success(f"✓ Created {len(collections)} special collections")

    return collections


def get_collection_summary(collections: Dict) -> Dict:
    """
    Get summary of special collections.

    Args:
        collections: Output from create_special_collections()

    Returns:
        Dictionary with summary
    """
    summary = {
        'total_collections': len(collections),
        'collections': []
    }

    for key, data in collections.items():
        summary['collections'].append({
            'key': key,
            'name': data['name'],
            'count': data['count']
        })

    return summary
