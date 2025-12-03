"""
Normalize raw site data into unified structure.

Orchestrates all attribute parsers to create complete, normalized site data.
"""

from typing import Dict, List, Set
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.b_01_transform import (
    parse_identity,
    parse_geographic,
    parse_descriptive,
    parse_classification,
    parse_temporal,
    parse_visual,
    parse_components,
)


def normalize_site(site: Dict, existing_keys: Set[str] = None) -> Dict:
    """
    Normalize a single heritage site into unified structure.

    Args:
        site: Raw site dictionary from JSON
        existing_keys: Set of already-generated keys for collision detection

    Returns:
        Normalized site dictionary with all attributes parsed

    Example:
        >>> raw_site = load_heritage_data()[0]
        >>> normalized = normalize_site(raw_site)
        >>> normalized['site_key']
        'butrint'
        >>> normalized['geography']['countries']['ALB']['name']
        'Albania'
    """
    if existing_keys is None:
        existing_keys = set()

    try:
        # Parse all attribute categories
        identity = parse_identity(site, existing_keys)
        geographic = parse_geographic(site)
        descriptive = parse_descriptive(site)
        classification = parse_classification(site)
        temporal = parse_temporal(site)
        visual = parse_visual(site)
        components = parse_components(site)

        # Build normalized structure
        normalized = {
            # Identity
            'site_key': identity['site_key'],
            'uuid': identity['uuid'],
            'unesco_id': identity['unesco_id'],
            'names': identity['names'],

            # Geographic
            'geography': {
                'coordinates': geographic['coordinates'],
                'countries': geographic['countries'],
                'region': geographic['region'],
                'is_transboundary': geographic['is_transboundary'],
                'country_count': geographic['country_count'],
            },

            # Descriptive
            'descriptions': {
                'short': descriptive['short_descriptions'],
                'full': descriptive['full_description'],
                'justification': descriptive['justification'],
            },

            # Classification
            'classification': {
                'category': classification['category'],
                'criteria': classification['criteria'],
                'area': classification['area'],
            },

            # Temporal
            'temporal': {
                'inscription': temporal['inscription'],
                'danger_status': temporal['danger_status'],
            },

            # Visual
            'visual': {
                'main_image': visual['main_image'],
                'gallery': visual['gallery'],
            },

            # Components
            'components': components,
        }

        return normalized

    except Exception as e:
        app_logger.error(
            f"Error normalizing site {site.get('name_en', 'Unknown')}: {e}"
        )
        raise


def normalize_all_sites(sites: List[Dict]) -> List[Dict]:
    """
    Normalize all sites in dataset.

    Args:
        sites: List of raw site dictionaries

    Returns:
        List of normalized site dictionaries

    Example:
        >>> raw_sites = load_heritage_data()
        >>> normalized_sites = normalize_all_sites(raw_sites)
        >>> len(normalized_sites)
        1248
    """
    app_logger.info(f"Normalizing {len(sites)} heritage sites...")

    normalized = []
    existing_keys = set()
    errors = []

    for idx, site in enumerate(sites):
        try:
            normalized_site = normalize_site(site, existing_keys)
            normalized.append(normalized_site)
            existing_keys.add(normalized_site['site_key'])

        except Exception as e:
            errors.append({
                'index': idx,
                'name': site.get('name_en', 'Unknown'),
                'uuid': site.get('uuid'),
                'error': str(e)
            })
            app_logger.error(f"Failed to normalize site {idx}: {site.get('name_en')}")

    # Report results
    success_count = len(normalized)
    error_count = len(errors)

    if error_count == 0:
        app_logger.success(f"✓ Successfully normalized all {success_count} sites")
    else:
        app_logger.warning(
            f"Normalized {success_count}/{len(sites)} sites ({error_count} errors)"
        )
        for error in errors[:5]:  # Show first 5 errors
            app_logger.error(f"  - {error['name']}: {error['error']}")

    return normalized


def build_site_index(normalized_sites: List[Dict]) -> Dict:
    """
    Build lookup indexes for normalized sites.

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with multiple indexes for fast lookups

    Indexes:
        - by_key: {site_key: site}
        - by_uuid: {uuid: site}
        - by_unesco_id: {unesco_id: site}

    Example:
        >>> sites = normalize_all_sites(load_heritage_data())
        >>> indexes = build_site_index(sites)
        >>> site = indexes['by_key']['butrint']
    """
    app_logger.info("Building site indexes...")

    indexes = {
        'by_key': {},
        'by_uuid': {},
        'by_unesco_id': {},
    }

    for site in normalized_sites:
        key = site['site_key']
        uuid = site['uuid']
        unesco_id = site['unesco_id']

        indexes['by_key'][key] = site
        indexes['by_uuid'][uuid] = site
        indexes['by_unesco_id'][unesco_id] = site

    app_logger.success(f"✓ Built indexes for {len(normalized_sites)} sites")

    return indexes


def get_normalization_stats(normalized_sites: List[Dict]) -> Dict:
    """
    Get statistics about normalized dataset.

    Args:
        normalized_sites: List of normalized sites

    Returns:
        Dictionary with statistics

    Example:
        >>> sites = normalize_all_sites(load_heritage_data())
        >>> stats = get_normalization_stats(sites)
        >>> stats['total_sites']
        1248
    """
    from collections import Counter

    stats = {
        'total_sites': len(normalized_sites),
        'by_category': Counter(),
        'by_region': Counter(),
        'by_country': Counter(),
        'transboundary_count': 0,
        'endangered_count': 0,
        'with_coordinates': 0,
        'with_area': 0,
        'with_main_image': 0,
        'multi_component_count': 0,
    }

    for site in normalized_sites:
        # Category
        category = site['classification']['category']['name']
        stats['by_category'][category] += 1

        # Region
        region = site['geography']['region']['code']
        stats['by_region'][region] += 1

        # Countries
        for country_code in site['geography']['countries'].keys():
            stats['by_country'][country_code] += 1

        # Transboundary
        if site['geography']['is_transboundary']:
            stats['transboundary_count'] += 1

        # Endangered
        if site['temporal']['danger_status']['is_endangered']:
            stats['endangered_count'] += 1

        # Coordinates
        if site['geography']['coordinates']['available']:
            stats['with_coordinates'] += 1

        # Area
        if site['classification']['area']['available']:
            stats['with_area'] += 1

        # Main image
        if site['visual']['main_image']['available']:
            stats['with_main_image'] += 1

        # Multi-component
        if site['components']['count'] > 1:
            stats['multi_component_count'] += 1

    return stats
