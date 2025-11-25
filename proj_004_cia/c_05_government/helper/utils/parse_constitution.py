import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_constitution(iso3Code: str) -> dict:
    """Parse constitution data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Constitution', {})

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'history' in test_data:
            history_data = test_data['history']
            if isinstance(history_data, dict) and 'text' in history_data:
                result['constitution_history'] = clean_text(history_data['text'])
            elif isinstance(history_data, str):
                result['constitution_history'] = clean_text(history_data)

        if 'amendments' in test_data:
            amendments_data = test_data['amendments']
            if isinstance(amendments_data, dict) and 'text' in amendments_data:
                result['constitution_amendments'] = clean_text(amendments_data['text'])
            elif isinstance(amendments_data, str):
                result['constitution_amendments'] = clean_text(amendments_data)

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['constitution_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing constitution for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_constitution")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'JPN', 'IND']:
        print(f"\n{iso3}:")
        try:
            result = parse_constitution(iso3)
            if result:
                hist = result.get('constitution_history', 'N/A')
                print(f"  History: {hist[:70]}..." if len(hist) > 70 else f"  History: {hist}")
                if 'constitution_amendments' in result:
                    print(f"  Has amendments info: Yes")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
