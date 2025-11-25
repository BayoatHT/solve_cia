import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_independence(iso3Code: str) -> dict:
    """Parse independence data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Independence', {})

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['independence_description'] = clean_text(text)

                # Try to extract date
                date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4}|\d{4})', text)
                if date_match:
                    result['independence_date'] = date_match.group(1)

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['independence_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing independence for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_independence")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'IND', 'BRA', 'MEX', 'AUS']:
        print(f"\n{iso3}:")
        try:
            result = parse_independence(iso3)
            if result:
                desc = result.get('independence_description', 'N/A')
                print(f"  Date: {result.get('independence_date', 'N/A')}")
                print(f"  Desc: {desc[:60]}..." if len(desc) > 60 else f"  Desc: {desc}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
