import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_government_type(iso3Code: str) -> dict:
    """Parse government type data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Government type', {})

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        # Extract main text
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['government_type'] = clean_text(text)

                # Extract government categories
                categories = _categorize_government_type(text)
                if categories:
                    result['government_categories'] = categories

        # Handle note
        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['government_type_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing government type for {iso3Code}: {e}")

    return result


def _categorize_government_type(text: str) -> list:
    """Categorize government type based on keywords."""
    if not text:
        return []

    text_lower = text.lower()
    categories = []

    type_patterns = {
        'republic': ['republic', 'republican'],
        'monarchy': ['monarchy', 'kingdom', 'sultanate', 'emirate'],
        'constitutional': ['constitutional'],
        'federal': ['federal', 'federation'],
        'parliamentary': ['parliamentary', 'parliament'],
        'presidential': ['presidential'],
        'communist': ['communist', 'marxist', 'socialist state'],
        'authoritarian': ['authoritarian', 'dictatorship'],
        'theocratic': ['theocratic', 'islamic republic', 'religious'],
        'democracy': ['democracy', 'democratic'],
        'unitary': ['unitary'],
        'territory': ['territory', 'dependency', 'overseas'],
    }

    for category, patterns in type_patterns.items():
        if any(p in text_lower for p in patterns):
            categories.append(category)

    return categories


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_government_type")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'SAU']:
        print(f"\n{iso3}:")
        try:
            result = parse_government_type(iso3)
            if result:
                print(f"  Type: {result.get('government_type', 'N/A')}")
                print(f"  Categories: {result.get('government_categories', [])}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
