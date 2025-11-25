import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_flag_description(iso3Code: str, return_original: bool = False)-> dict:
    """Parse flag description from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Flag description', {})

    if return_original:
        return test_data


    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['flag_description'] = clean_text(text)
                colors = _extract_flag_colors(text)
                if colors:
                    result['flag_colors'] = colors

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['flag_description_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing flag description for {iso3Code}: {e}")

    return result


def _extract_flag_colors(text: str) -> list:
    """Extract colors mentioned in flag description."""
    if not text:
        return []
    text_lower = text.lower()
    color_keywords = [
        'red', 'blue', 'green', 'yellow', 'white', 'black', 'orange',
        'gold', 'purple', 'brown', 'pink', 'cyan', 'maroon', 'navy',
        'scarlet', 'crimson', 'azure', 'cerulean', 'saffron'
    ]
    return [color for color in color_keywords if color in text_lower]


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_flag_description")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'JPN', 'IND']:
        print(f"\n{iso3}:")
        try:
            result = parse_flag_description(iso3)
            if result:
                print(f"  Colors: {result.get('flag_colors', [])}")
                desc = result.get('flag_description', 'N/A')
                print(f"  Desc: {desc[:60]}...")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
