import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_executive_branch(iso3Code: str) -> dict:
    """Parse executive branch data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Executive branch', {})

    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        field_mappings = {
            'chief of state': 'chief_of_state',
            'head of government': 'head_of_government',
            'cabinet': 'cabinet',
            'elections/appointments': 'elections_appointments',
            'election results': 'election_results',
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
                result['executive_branch_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing executive branch for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_executive_branch")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'RUS']:
        print(f"\n{iso3}:")
        try:
            result = parse_executive_branch(iso3)
            if result:
                chief = result.get('chief_of_state', 'N/A')
                head = result.get('head_of_government', 'N/A')
                print(f"  Chief: {chief[:50]}..." if len(chief) > 50 else f"  Chief: {chief}")
                print(f"  Head: {head[:50]}..." if len(head) > 50 else f"  Head: {head}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
