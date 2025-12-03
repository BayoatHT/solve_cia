"""
Normalization module for World Heritage sites.

Combines all attribute parsers into unified, normalized site structures.
"""

from .normalize_site import (
    normalize_site,
    normalize_all_sites,
    build_site_index,
    get_normalization_stats
)
from .validate_site import validate_site, validate_all_sites, check_duplicate_keys

__all__ = [
    'normalize_site',
    'normalize_all_sites',
    'build_site_index',
    'get_normalization_stats',
    'validate_site',
    'validate_all_sites',
    'check_duplicate_keys',
]
