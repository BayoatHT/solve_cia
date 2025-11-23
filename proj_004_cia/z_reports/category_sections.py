"""
Category Sections Utility

Provides a dictionary of all CIA World Factbook categories and their sections,
for both raw data keys and parsed output keys.

Usage:
    from proj_004_cia.z_reports.category_sections import (
        RAW_CATEGORIES,
        PARSED_CATEGORIES,
        get_raw_sections,
        get_parsed_sections
    )
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Dict, List, Callable
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

# Import all return_*_data functions for parsed data
from proj_004_cia.c_01_intoduction.return_introduction_data import return_introduction_data
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data
from proj_004_cia.c_03_society.return_society_data import return_society_data
from proj_004_cia.c_04_environment.return_environment_data import return_environment_data
from proj_004_cia.c_05_government.return_government_data import return_government_data
from proj_004_cia.c_06_economy.return_economy_data import return_economy_data
from proj_004_cia.c_07_energy.return_energy_data import return_energy_data
from proj_004_cia.c_08_communications.return_communications_data import return_communications_data
from proj_004_cia.c_09_transportation.return_transportation_data import return_transportation_data
from proj_004_cia.c_10_military.return_military_data import return_military_data
from proj_004_cia.c_11_space.return_space_data import return_space_data
from proj_004_cia.c_12_terrorism.return_terrorism_data import return_terrorism_data
from proj_004_cia.c_13_issues.return_issues_data import return_issues_data


# Map raw category names to parser functions
CATEGORY_PARSERS: Dict[str, Callable] = {
    'Introduction': return_introduction_data,
    'Geography': return_geography_data,
    'People and Society': return_society_data,
    'Environment': return_environment_data,
    'Government': return_government_data,
    'Economy': return_economy_data,
    'Energy': return_energy_data,
    'Communications': return_communications_data,
    'Transportation': return_transportation_data,
    'Military and Security': return_military_data,
    'Space': return_space_data,
    'Terrorism': return_terrorism_data,
    'Transnational Issues': return_issues_data,
}


def _build_raw_categories() -> Dict[str, List[str]]:
    """Build dictionary of raw categories and their section keys from sample data."""
    data = load_country_data('USA')
    categories = {}
    for cat_name, cat_data in data.items():
        if isinstance(cat_data, dict):
            categories[cat_name] = sorted(list(cat_data.keys()))
    return categories


def _build_parsed_categories() -> Dict[str, List[str]]:
    """Build dictionary of parsed categories and their output keys."""
    categories = {}
    for cat_name, parser in CATEGORY_PARSERS.items():
        try:
            data = load_country_data('USA')
            result = parser(data, 'USA')
            if isinstance(result, dict):
                categories[cat_name] = sorted(list(result.keys()))
            else:
                categories[cat_name] = []
        except Exception:
            categories[cat_name] = []
    return categories


# Build the category dictionaries
RAW_CATEGORIES: Dict[str, List[str]] = _build_raw_categories()
PARSED_CATEGORIES: Dict[str, List[str]] = _build_parsed_categories()


def get_raw_sections(category: str) -> List[str]:
    """Get list of raw section keys for a category."""
    return RAW_CATEGORIES.get(category, [])


def get_parsed_sections(category: str) -> List[str]:
    """Get list of parsed output keys for a category."""
    return PARSED_CATEGORIES.get(category, [])


def get_parser(category: str) -> Callable:
    """Get the parser function for a category."""
    return CATEGORY_PARSERS.get(category)


def list_all_raw() -> None:
    """Print all raw categories and sections."""
    print("\nRAW Categories and Sections:")
    print("=" * 60)
    for cat in sorted(RAW_CATEGORIES.keys()):
        print(f"\n{cat}:")
        for sec in RAW_CATEGORIES[cat]:
            print(f"    - {sec}")


def list_all_parsed() -> None:
    """Print all parsed categories and sections."""
    print("\nPARSED Categories and Sections:")
    print("=" * 60)
    for cat in sorted(PARSED_CATEGORIES.keys()):
        print(f"\n{cat}:")
        for sec in PARSED_CATEGORIES[cat]:
            print(f"    - {sec}")


if __name__ == "__main__":
    print("RAW_CATEGORIES =", RAW_CATEGORIES)
    print("\nPARSED_CATEGORIES =", PARSED_CATEGORIES)
    print("\n" + "=" * 60)
    list_all_raw()
    print("\n" + "=" * 60)
    list_all_parsed()
