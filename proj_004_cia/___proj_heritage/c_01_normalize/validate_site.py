"""
Validate normalized site data.

Ensures normalized sites meet quality and completeness standards.
"""

from typing import Dict, List
from proj_004_cia.__logger.logger import app_logger


def validate_site(site: Dict) -> Dict:
    """
    Validate normalized site data.

    Args:
        site: Normalized site dictionary

    Returns:
        Dictionary with validation results

    Example:
        >>> normalized = normalize_site(raw_site)
        >>> validation = validate_site(normalized)
        >>> validation['valid']
        True
    """
    errors = []
    warnings = []

    # Required top-level fields
    required_fields = ['site_key', 'uuid', 'unesco_id', 'names', 'geography',
                       'descriptions', 'classification', 'temporal', 'visual', 'components']

    for field in required_fields:
        if field not in site:
            errors.append(f"Missing required field: {field}")

    # Validate site_key
    if 'site_key' in site:
        key = site['site_key']
        if not key or len(key) < 2:
            errors.append(f"Invalid site_key: {key}")
        if not all(c.islower() or c.isdigit() or c == '_' for c in key):
            errors.append(f"site_key contains invalid characters: {key}")

    # Validate names
    if 'names' in site:
        if 'en' not in site['names'] or not site['names']['en']:
            errors.append("Missing English name")

    # Validate geography
    if 'geography' in site:
        geo = site['geography']

        # Coordinates
        if not geo.get('coordinates', {}).get('available'):
            warnings.append("Missing coordinates")

        # Countries
        if not geo.get('countries'):
            errors.append("No countries defined")

        # Region
        if not geo.get('region', {}).get('code'):
            errors.append("Missing region code")

    # Validate classification
    if 'classification' in site:
        cls = site['classification']

        # Category
        category = cls.get('category', {}).get('name')
        if category not in ['Cultural', 'Natural', 'Mixed']:
            errors.append(f"Invalid category: {category}")

        # Criteria
        criteria = cls.get('criteria', {})
        if criteria.get('count', 0) == 0:
            warnings.append("No criteria defined")

        # Area
        if not cls.get('area', {}).get('available'):
            warnings.append("Missing area data")

    # Validate temporal
    if 'temporal' in site:
        temp = site['temporal']

        # Inscription
        inscription = temp.get('inscription', {})
        if not inscription.get('primary_date'):
            errors.append("Missing inscription date")

    # Validate visual
    if 'visual' in site:
        vis = site['visual']

        # Main image
        if not vis.get('main_image', {}).get('available'):
            warnings.append("Missing main image")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'error_count': len(errors),
        'warning_count': len(warnings),
    }


def validate_all_sites(normalized_sites: List[Dict]) -> Dict:
    """
    Validate all normalized sites.

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with validation summary

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> validation = validate_all_sites(sites)
        >>> validation['valid_count']
        1248
    """
    app_logger.info(f"Validating {len(normalized_sites)} normalized sites...")

    results = {
        'total_sites': len(normalized_sites),
        'valid_count': 0,
        'error_count': 0,
        'warning_count': 0,
        'sites_with_errors': [],
        'sites_with_warnings': [],
    }

    for site in normalized_sites:
        validation = validate_site(site)

        if validation['valid']:
            results['valid_count'] += 1
        else:
            results['error_count'] += 1
            results['sites_with_errors'].append({
                'site_key': site.get('site_key'),
                'name': site.get('names', {}).get('en', 'Unknown'),
                'errors': validation['errors']
            })

        if validation['warnings']:
            results['warning_count'] += 1
            results['sites_with_warnings'].append({
                'site_key': site.get('site_key'),
                'name': site.get('names', {}).get('en', 'Unknown'),
                'warnings': validation['warnings']
            })

    # Report results
    if results['error_count'] == 0:
        app_logger.success(f"✓ All {results['valid_count']} sites are valid")
    else:
        app_logger.error(
            f"✗ {results['error_count']} sites have errors"
        )
        # Show first 3 errors
        for site in results['sites_with_errors'][:3]:
            app_logger.error(f"  - {site['name']}: {site['errors']}")

    if results['warning_count'] > 0:
        app_logger.warning(
            f"⚠ {results['warning_count']} sites have warnings"
        )

    return results


def check_duplicate_keys(normalized_sites: List[Dict]) -> Dict:
    """
    Check for duplicate site keys.

    Args:
        normalized_sites: List of normalized sites

    Returns:
        Dictionary with duplicate check results

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> check = check_duplicate_keys(sites)
        >>> check['has_duplicates']
        False
    """
    from collections import Counter

    keys = [site['site_key'] for site in normalized_sites]
    key_counts = Counter(keys)

    duplicates = {key: count for key, count in key_counts.items() if count > 1}

    return {
        'has_duplicates': len(duplicates) > 0,
        'duplicate_count': len(duplicates),
        'duplicates': duplicates
    }
