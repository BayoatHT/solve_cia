import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_legal_system(iso3Code: str, return_original: bool = False)-> dict:
    """Parse legal system data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Legal system', {})

    if return_original:
        return test_data


    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        # Extract main legal system description
        if 'text' in test_data:
            legal_text = test_data['text']
            if isinstance(legal_text, str) and legal_text.strip():
                cleaned_text = clean_text(legal_text)
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
                cleaned_note = clean_text(note_data)
                if cleaned_note:
                    result['legal_system_note'] = cleaned_note

    except Exception as e:
        logger.error(f"Error parsing legal system for {iso3Code}: {e}")

    return result


def _extract_legal_system_types(text: str) -> list:
    """Extract and categorize legal system types from description."""
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


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_legal_system")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'SAU', 'IRN']:
        print(f"\n{iso3}:")
        try:
            result = parse_legal_system(iso3)
            if result:
                desc = result.get('legal_system_description', 'N/A')
                print(f"  Types: {result.get('legal_system_types', [])}")
                print(f"  Desc: {desc[:60]}..." if len(desc) > 60 else f"  Desc: {desc}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
