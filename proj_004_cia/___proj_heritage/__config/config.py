"""
Configuration settings for World Heritage data processing.

Contains constants, enumerations, and configuration for the heritage system.
"""

import os
from pathlib import Path
from typing import Dict, List

# Base paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "_raw_data" / "json"
DOCS_DIR = BASE_DIR / "_docs"
PRODUCT_DIR = BASE_DIR / "y_to_product"

# Raw data file
RAW_DATA_FILE = RAW_DATA_DIR / "all_world_heritage.json"

# Supported languages
LANGUAGES: List[str] = ['en', 'fr', 'es', 'ru', 'ar', 'zh']

# UNESCO regions
REGIONS: Dict[str, str] = {
    'EUR': 'Europe and North America',
    'ASP': 'Asia and the Pacific',
    'LAC': 'Latin America and the Caribbean',
    'AFR': 'Africa',
    'ARB': 'Arab States',
}

# Heritage categories
CATEGORIES: Dict[int, str] = {
    1: 'Cultural',
    2: 'Natural',
    3: 'Mixed',
}

# Criteria mapping
CRITERIA_MAPPING: Dict[str, str] = {
    'c1': '(i)',
    'c2': '(ii)',
    'c3': '(iii)',
    'c4': '(iv)',
    'c5': '(v)',
    'c6': '(vi)',
    'n7': '(vii)',
    'n8': '(viii)',
    'n9': '(ix)',
    'n10': '(x)',
}

# Criteria descriptions
CRITERIA_DESCRIPTIONS: Dict[str, str] = {
    'c1': 'Masterpiece of human creative genius',
    'c2': 'Interchange of human values',
    'c3': 'Testimony to cultural tradition',
    'c4': 'Significant stage in human history',
    'c5': 'Traditional human settlement',
    'c6': 'Associated with events or traditions',
    'n7': 'Natural beauty or phenomena',
    'n8': 'Geological or geomorphic features',
    'n9': 'Ecological processes',
    'n10': 'Biodiversity and species conservation',
}


class Config:
    """
    Configuration class for World Heritage system.
    """

    # Paths
    BASE_DIR = BASE_DIR
    RAW_DATA_DIR = RAW_DATA_DIR
    RAW_DATA_FILE = RAW_DATA_FILE
    DOCS_DIR = DOCS_DIR
    PRODUCT_DIR = PRODUCT_DIR

    # Languages
    LANGUAGES = LANGUAGES
    DEFAULT_LANGUAGE = 'en'

    # Regions
    REGIONS = REGIONS
    REGION_CODES = list(REGIONS.keys())

    # Categories
    CATEGORIES = CATEGORIES
    CATEGORY_NAMES = list(CATEGORIES.values())

    # Criteria
    CRITERIA_MAPPING = CRITERIA_MAPPING
    CRITERIA_DESCRIPTIONS = CRITERIA_DESCRIPTIONS

    # Processing settings
    EXPECTED_SITE_COUNT = 1248
    MAX_COMPONENTS_TO_PARSE = 150  # Safety limit for parsing

    # Output settings
    PRETTY_JSON = True
    JSON_INDENT = 2

    @classmethod
    def get_product_path(cls, category: str) -> Path:
        """
        Get path for product output by category.

        Args:
            category: Product category (e.g., 'sites_by_key', 'sites_by_country')

        Returns:
            Path to product directory
        """
        return cls.PRODUCT_DIR / category

    @classmethod
    def ensure_product_dirs(cls) -> None:
        """
        Ensure all product directories exist.
        """
        product_categories = [
            'sites_by_key',
            'sites_by_country',
            'sites_by_region',
            'sites_by_category',
            'special_collections',
            'complete',
        ]

        for category in product_categories:
            path = cls.get_product_path(category)
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def validate_raw_data(cls) -> bool:
        """
        Validate that raw data file exists.

        Returns:
            True if raw data file exists, False otherwise
        """
        return cls.RAW_DATA_FILE.exists()


# Export constants for easy access
__all__ = [
    'Config',
    'LANGUAGES',
    'REGIONS',
    'CATEGORIES',
    'CRITERIA_MAPPING',
    'CRITERIA_DESCRIPTIONS',
]
