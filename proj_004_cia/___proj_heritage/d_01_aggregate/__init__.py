"""
Aggregation module for World Heritage sites.

Groups and organizes sites by various attributes:
- by_country: Sites grouped by country (ISO3)
- by_region: Sites grouped by UNESCO region
- by_category: Sites grouped by category (Cultural/Natural/Mixed)
- by_criteria: Sites grouped by specific criteria
- special_collections: Transboundary, endangered, etc.
"""

from .by_country import aggregate_by_country
from .by_region import aggregate_by_region
from .by_category import aggregate_by_category
from .by_criteria import aggregate_by_criteria
from .special_collections import create_special_collections

__all__ = [
    'aggregate_by_country',
    'aggregate_by_region',
    'aggregate_by_category',
    'aggregate_by_criteria',
    'create_special_collections',
]
