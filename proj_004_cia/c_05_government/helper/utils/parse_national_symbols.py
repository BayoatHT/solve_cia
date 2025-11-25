import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_national_symbols(iso3Code: str, return_original: bool = False)-> dict:
    """Parse national symbols from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('National symbol(s)', {})

    if return_original:
        return test_data


    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['national_symbols'] = clean_text(text)
                colors = _extract_colors(text)
                if colors:
                    result['national_colors'] = colors

        field_mappings = {
            'national symbol(s)': 'national_symbols',
            'national colors': 'national_colors',
        }
        for cia_key, output_key in field_mappings.items():
            if cia_key in test_data:
                field_data = test_data[cia_key]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    if text and isinstance(text, str):
                        result[output_key] = clean_text(text)
                elif isinstance(field_data, str) and field_data.strip():
                    result[output_key] = clean_text(field_data)

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['national_symbols_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing national symbols for {iso3Code}: {e}")

    return result


def _extract_colors(text: str) -> list:
    """Extract national colors from text."""
    if not text:
        return []
    color_match = re.search(r'national colors?:?\s*([^;]+)', text.lower())
    if color_match:
        colors_text = color_match.group(1)
        colors = [c.strip() for c in colors_text.split(',')]
        return [c for c in colors if c and len(c) < 20]
    return []


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_national_symbols")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'JPN', 'IND']:
        print(f"\n{iso3}:")
        try:
            result = parse_national_symbols(iso3)
            if result:
                print(f"  Symbols: {result.get('national_symbols', 'N/A')[:50]}...")
                print(f"  Colors: {result.get('national_colors', [])}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
