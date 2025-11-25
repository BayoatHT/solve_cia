import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_political_parties(iso3Code: str) -> dict:
    """Parse political parties data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Political parties', {})

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['political_parties'] = clean_text(text)
        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['political_parties_note'] = clean_text(note)
    except Exception as e:
        logger.error(f"Error parsing political parties for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_political_parties")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'JPN', 'IND']:
        print(f"\n{iso3}:")
        try:
            result = parse_political_parties(iso3)
            if result:
                parties = result.get('political_parties', 'N/A')
                print(f"  Parties: {parties[:70]}..." if len(parties) > 70 else f"  Parties: {parties}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
