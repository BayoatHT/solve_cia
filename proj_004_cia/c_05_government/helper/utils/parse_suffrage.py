import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_suffrage(iso3Code: str) -> dict:
    """Parse suffrage data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Suffrage', {})

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['suffrage_description'] = clean_text(text)

                # Try to extract voting age
                age_match = re.search(r'(\d{1,2})\s*years?\s*of\s*age', text.lower())
                if age_match:
                    result['voting_age'] = int(age_match.group(1))

                # Check if universal
                if 'universal' in text.lower():
                    result['universal_suffrage'] = True
                if 'compulsory' in text.lower():
                    result['compulsory_voting'] = True

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['suffrage_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing suffrage for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_suffrage")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'AUS', 'BRA', 'SAU']:
        print(f"\n{iso3}:")
        try:
            result = parse_suffrage(iso3)
            if result:
                print(f"  Voting age: {result.get('voting_age', 'N/A')}")
                print(f"  Universal: {result.get('universal_suffrage', False)}")
                print(f"  Compulsory: {result.get('compulsory_voting', False)}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
