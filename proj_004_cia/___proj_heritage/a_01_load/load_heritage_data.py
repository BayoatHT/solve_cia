"""
Load World Heritage data from JSON file.

Primary data loading function for the heritage system.
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.config import Config


def load_heritage_data(file_path: Optional[Path] = None) -> List[Dict]:
    """
    Load World Heritage sites data from JSON file.

    Args:
        file_path: Optional path to JSON file (defaults to Config.RAW_DATA_FILE)

    Returns:
        List of site dictionaries

    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON is invalid

    Example:
        >>> sites = load_heritage_data()
        >>> len(sites)
        1248
    """
    if file_path is None:
        file_path = Config.RAW_DATA_FILE

    app_logger.info(f"Loading World Heritage data from: {file_path}")

    # Check file exists
    if not file_path.exists():
        app_logger.error(f"Data file not found: {file_path}")
        raise FileNotFoundError(f"Heritage data file not found: {file_path}")

    try:
        # Load JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate it's a list
        if not isinstance(data, list):
            app_logger.error("Data is not a list")
            raise ValueError("Heritage data must be a list of sites")

        site_count = len(data)
        app_logger.success(f"✓ Loaded {site_count} heritage sites")

        # Warn if count unexpected
        if site_count != Config.EXPECTED_SITE_COUNT:
            app_logger.warning(
                f"Expected {Config.EXPECTED_SITE_COUNT} sites, found {site_count}"
            )

        return data

    except json.JSONDecodeError as e:
        app_logger.error(f"Invalid JSON in data file: {e}")
        raise

    except Exception as e:
        app_logger.error(f"Error loading heritage data: {e}")
        raise


def validate_dataset(sites: List[Dict]) -> Dict:
    """
    Validate loaded dataset for completeness and correctness.

    Args:
        sites: List of site dictionaries

    Returns:
        Dictionary with validation results

    Example:
        >>> sites = load_heritage_data()
        >>> validation = validate_dataset(sites)
        >>> validation['valid']
        True
    """
    app_logger.info("Validating heritage dataset...")

    results = {
        'total_sites': len(sites),
        'valid_sites': 0,
        'errors': [],
        'warnings': [],
        'missing_fields': {},
        'invalid_data': {}
    }

    # Required fields
    required_fields = [
        'uuid', 'id_no', 'name_en', 'iso_codes', 'category',
        'date_inscribed', 'region', 'transboundary'
    ]

    for idx, site in enumerate(sites):
        site_errors = []
        site_warnings = []

        # Check required fields
        for field in required_fields:
            if field not in site or site[field] is None:
                site_errors.append(f"Missing required field: {field}")
                results['missing_fields'][field] = results['missing_fields'].get(field, 0) + 1

        # Validate specific fields
        # UUID
        if 'uuid' in site and site['uuid']:
            if not isinstance(site['uuid'], str) or len(site['uuid']) < 10:
                site_errors.append("Invalid UUID format")

        # ISO codes
        if 'iso_codes' in site and site['iso_codes']:
            iso_codes = site['iso_codes']
            if not isinstance(iso_codes, str):
                site_errors.append("ISO codes must be string")

        # Category
        if 'category' in site:
            if site['category'] not in ['Cultural', 'Natural', 'Mixed']:
                site_errors.append(f"Invalid category: {site['category']}")

        # Coordinates (warning if missing, not error)
        if not site.get('coordinates'):
            site_warnings.append("Missing coordinates")

        # Area (warning if missing, not error)
        if site.get('area_hectares') is None:
            site_warnings.append("Missing area_hectares")

        # Main image (warning if missing, not error)
        if not site.get('main_image_url'):
            site_warnings.append("Missing main_image_url")

        # Add errors/warnings to results
        if site_errors:
            results['errors'].append({
                'site_index': idx,
                'name': site.get('name_en', 'Unknown'),
                'uuid': site.get('uuid'),
                'errors': site_errors
            })
        else:
            results['valid_sites'] += 1

        if site_warnings:
            results['warnings'].append({
                'site_index': idx,
                'name': site.get('name_en', 'Unknown'),
                'uuid': site.get('uuid'),
                'warnings': site_warnings
            })

    # Summary
    error_count = len(results['errors'])
    warning_count = len(results['warnings'])

    if error_count == 0:
        app_logger.success(f"✓ All {results['total_sites']} sites are valid")
    else:
        app_logger.error(f"✗ {error_count} sites have errors")

    if warning_count > 0:
        app_logger.warning(f"⚠ {warning_count} sites have warnings")

    # Log missing field summary
    if results['missing_fields']:
        app_logger.info("Missing field summary:")
        for field, count in results['missing_fields'].items():
            app_logger.info(f"  - {field}: {count} sites")

    return results


def get_site_by_uuid(sites: List[Dict], uuid: str) -> Optional[Dict]:
    """
    Get a site by its UUID.

    Args:
        sites: List of site dictionaries
        uuid: UUID to search for

    Returns:
        Site dictionary or None if not found

    Example:
        >>> sites = load_heritage_data()
        >>> site = get_site_by_uuid(sites, "1e6988b2-e175-509e-9e43-943ffeced51a")
        >>> site['name_en']
        'Butrint'
    """
    for site in sites:
        if site.get('uuid') == uuid:
            return site

    return None


def get_site_by_id(sites: List[Dict], id_no: str) -> Optional[Dict]:
    """
    Get a site by its UNESCO ID number.

    Args:
        sites: List of site dictionaries
        id_no: UNESCO ID to search for

    Returns:
        Site dictionary or None if not found

    Example:
        >>> sites = load_heritage_data()
        >>> site = get_site_by_id(sites, "570")
        >>> site['name_en']
        'Butrint'
    """
    for site in sites:
        if site.get('id_no') == id_no:
            return site

    return None


def filter_sites_by_category(sites: List[Dict], category: str) -> List[Dict]:
    """
    Filter sites by category.

    Args:
        sites: List of site dictionaries
        category: Category to filter by ('Cultural', 'Natural', 'Mixed')

    Returns:
        Filtered list of sites

    Example:
        >>> sites = load_heritage_data()
        >>> cultural = filter_sites_by_category(sites, 'Cultural')
        >>> len(cultural)
        972
    """
    return [s for s in sites if s.get('category') == category]


def filter_sites_by_region(sites: List[Dict], region_code: str) -> List[Dict]:
    """
    Filter sites by region code.

    Args:
        sites: List of site dictionaries
        region_code: Region code ('EUR', 'ASP', 'LAC', 'AFR', 'ARB')

    Returns:
        Filtered list of sites

    Example:
        >>> sites = load_heritage_data()
        >>> europe = filter_sites_by_region(sites, 'EUR')
        >>> len(europe)
        580
    """
    return [s for s in sites if s.get('region_code') == region_code]


def get_dataset_statistics(sites: List[Dict]) -> Dict:
    """
    Get statistical summary of the dataset.

    Args:
        sites: List of site dictionaries

    Returns:
        Dictionary with statistics

    Example:
        >>> sites = load_heritage_data()
        >>> stats = get_dataset_statistics(sites)
        >>> stats['total_sites']
        1248
    """
    from collections import Counter

    stats = {
        'total_sites': len(sites),
        'by_category': Counter(s.get('category') for s in sites),
        'by_region': Counter(s.get('region_code') for s in sites),
        'transboundary_count': sum(1 for s in sites if s.get('transboundary') == 'True'),
        'endangered_count': sum(1 for s in sites if s.get('danger') == 'True'),
        'missing_coordinates': sum(1 for s in sites if not s.get('coordinates')),
        'missing_area': sum(1 for s in sites if s.get('area_hectares') is None),
        'missing_main_image': sum(1 for s in sites if not s.get('main_image_url')),
        'date_range': {
            'earliest': min((int(s.get('date_inscribed', 9999)) for s in sites if s.get('date_inscribed')), default=None),
            'latest': max((int(s.get('date_inscribed', 0)) for s in sites if s.get('date_inscribed')), default=None),
        }
    }

    return stats
