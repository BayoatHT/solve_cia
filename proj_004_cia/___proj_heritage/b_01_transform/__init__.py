"""
Attribute transformation module for World Heritage sites.

Organized by attribute categories:
- identity: Names, keys, identifiers
- geographic: Location, countries, regions
- descriptive: Descriptions, justifications
- classification: Categories, criteria, area
- temporal: Dates, danger status
- visual: Images, galleries
- components: Multi-location site components
"""

from .identity import parse_identity
from .geographic import parse_geographic
from .descriptive import parse_descriptive
from .classification import parse_classification
from .temporal import parse_temporal
from .visual import parse_visual
from .components import parse_components
from .enhancements import parse_enhancements

__all__ = [
    'parse_identity',
    'parse_geographic',
    'parse_descriptive',
    'parse_classification',
    'parse_temporal',
    'parse_visual',
    'parse_components',
    'parse_enhancements',
]
