#!/usr/bin/env python3
"""
CIA Government Section Parser: Legal System
==========================================

Implementation for the existing parse_legal_system function.
Updates the stub function with production-ready parsing logic.

Based on Analysis:
- Coverage: 97.6% (246 countries)  
- Complexity Score: 246 (moderate)
- Priority Score: 730.19 (highest priority)
- Parsing Challenges: text_note_extraction(246)
"""

import re
import json
from typing import Dict, List, Any, Optional
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils._inspect_cia_property_data import inspect_cia_property_data
# --------------------------------------------------------------------------------------------------------


def parse_legal_system(
    test_data: dict,
    iso3Code: str = None
) -> dict:
    """
    Parse legal system data from CIA Government section.

    Based on analysis, this function handles:
    - text_note_extraction (246 instances)
    - HTML tag cleaning
    - Note extraction
    - Simple nested dictionary structure

    Args:
        test_data: Dictionary containing legal system data with 'text' and optional 'note' keys

    Returns:
        Dictionary with parsed legal system information

    Examples:
        >>> data = {"text": "civil legal system based on French civil law"}
        >>> result = parse_legal_system(data)
        >>> # Returns structured legal system data
    """

    result = {}

    # Input validation
    if not test_data or not isinstance(test_data, dict):
        app_logger.warning(f"Invalid legal system data: {test_data}")
        return result

    try:
        # Extract main legal system description
        if 'text' in test_data:
            legal_text = test_data['text']
            if isinstance(legal_text, str) and legal_text.strip():
                # Clean the text
                cleaned_text = _clean_legal_system_text(legal_text)
                if cleaned_text:
                    result['legal_system_description'] = cleaned_text

                    # Extract key legal system types for categorization
                    system_types = _extract_legal_system_types(cleaned_text)
                    if system_types:
                        result['legal_system_types'] = system_types

        # Extract notes if present
        if 'note' in test_data:
            note_data = test_data['note']
            if isinstance(note_data, str) and note_data.strip():
                cleaned_note = _clean_legal_system_text(note_data)
                if cleaned_note:
                    result['legal_system_note'] = cleaned_note

        # Add metadata
        if result:
            result['data_source'] = 'CIA_World_Factbook'
            result['extraction_confidence'] = 'high' if 'legal_system_description' in result else 'low'

    except Exception as e:
        app_logger.error(f"Error parsing legal system: {e}")
        # Return empty dict on error to maintain consistency

    return result


def _clean_legal_system_text(text: str) -> str:
    """
    Clean legal system text by removing HTML tags and normalizing content.

    Args:
        text: Raw text from CIA JSON

    Returns:
        Cleaned text string
    """
    if not text or not isinstance(text, str):
        return ""

    # Remove HTML tags (common in CIA data)
    cleaned = re.sub(r'<[^>]+>', '', text)

    # Replace HTML entities
    html_entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&rsquo;': "'",
        '&lsquo;': "'",
        '&ldquo;': '"',
        '&rdquo;': '"',
        '&ndash;': '-',
        '&mdash;': '—',
        '&nbsp;': ' ',
        '&ecirc;': 'ê',
        '&acirc;': 'â'
    }

    for entity, replacement in html_entities.items():
        cleaned = cleaned.replace(entity, replacement)

    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    return cleaned


def _extract_legal_system_types(text: str) -> list:
    """
    Extract and categorize legal system types from description.

    Args:
        text: Cleaned legal system description

    Returns:
        List of identified legal system types
    """
    if not text:
        return []

    text_lower = text.lower()
    system_types = []

    # Common legal system patterns
    legal_patterns = {
        'civil_law': ['civil law', 'civil code', 'napoleonic', 'romano-germanic'],
        'common_law': ['common law', 'english common law', 'british common law'],
        'islamic_law': ['islamic law', 'sharia', 'shariah', 'islamic legal'],
        'customary_law': ['customary law', 'traditional law', 'tribal law'],
        'socialist_law': ['socialist law', 'soviet', 'marxist'],
        'mixed_system': ['mixed', 'hybrid', 'combination'],
        'religious_law': ['religious law', 'canon law', 'talmudic'],
        'federal_system': ['federal', 'state legal systems']
    }

    for system_type, patterns in legal_patterns.items():
        if any(pattern in text_lower for pattern in patterns):
            system_types.append(system_type)

    return system_types


# Example usage and testing
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    section_key = 'Government'
    property_key = 'Legal system'
    # --------------------------------------------------------------------------------------------------
    # List of countries to test
    test_countries = ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'IND'
                      'RUS', 'BRA', 'JPN', 'AUS', 'CAN', 'MEX'
                      'ZAF', 'KOR', 'ITA', 'ESP', 'NLD', 'SWE',
                      'NOR', 'FIN', 'DNK', 'POL', 'TUR', 'ARG',
                      'CHL', 'PER', 'COL', 'VEN', 'EGY', 'SAR',
                      'UAE', 'ISR', 'IRN', 'PAK', 'BGD', 'PHL',
                      'IDN', 'MYS', 'THA', 'VNM', 'SGP', 'NZL',
                      'KHM', 'MMR', 'LKA', 'NPL', 'BTN', 'MDV',
                      'KAZ', 'UZB', 'TKM', 'KGZ', 'TJK', 'AZE',
                      'GEO', 'ARM', 'MDA', 'UKR', 'BLR', 'LVA',]
    # --------------------------------------------------------------------------------------------------
    test_legal_system_data = inspect_cia_property_data(
        section_key=section_key,
        property_key=property_key,
        countries=test_countries,
        limit_countries=30
    )
    print(f"Test Legal system Orginal Data")
    for index, country_data in enumerate(test_legal_system_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            print(f"Original Data: {data}")
    # --------------------------------------------------------------------------------------------------
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    print("Testing legal_system Parser")
    print("=" * 50)

    for index, country_data in enumerate(test_legal_system_data, 1):
        for iso3_code, data in country_data.items():
            print(f"\n{index}. {iso3_code}")
            print("-" * 30)
            result = parse_legal_system(
                test_data=data, iso3Code=iso3_code)

            # Pretty print the result

            print(json.dumps(result, indent=2, ensure_ascii=False))

            # Validate structure
            assert isinstance(result, dict)
            print("✅ Structure validation passed")
