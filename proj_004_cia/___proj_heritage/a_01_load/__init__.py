"""
Data loading module for World Heritage sites.

Handles loading and initial validation of raw JSON data.
"""

from .load_heritage_data import (
    load_heritage_data,
    validate_dataset,
    get_dataset_statistics,
    get_site_by_uuid,
    get_site_by_id,
    filter_sites_by_category,
    filter_sites_by_region,
)

__all__ = [
    'load_heritage_data',
    'validate_dataset',
    'get_dataset_statistics',
    'get_site_by_uuid',
    'get_site_by_id',
    'filter_sites_by_category',
    'filter_sites_by_region',
]
