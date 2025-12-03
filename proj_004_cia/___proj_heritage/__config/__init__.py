"""
Configuration module for World Heritage data processing.

This module provides:
- ISO country code mappings (ISO2 ↔ ISO3)
- Configuration settings
- Constants and enumerations
"""

from .iso_mapping import (
    ISO2_TO_ISO3,
    ISO3_TO_ISO2,
    ISO3_TO_COUNTRY_NAME,
    get_country_info,
    convert_iso2_to_iso3,
    convert_iso3_to_iso2,
)

from .config import (
    Config,
    LANGUAGES,
    REGIONS,
    CATEGORIES,
    CRITERIA_MAPPING,
)

__all__ = [
    # ISO mappings
    'ISO2_TO_ISO3',
    'ISO3_TO_ISO2',
    'ISO3_TO_COUNTRY_NAME',
    'get_country_info',
    'convert_iso2_to_iso3',
    'convert_iso3_to_iso2',

    # Configuration
    'Config',
    'LANGUAGES',
    'REGIONS',
    'CATEGORIES',
    'CRITERIA_MAPPING',
]
