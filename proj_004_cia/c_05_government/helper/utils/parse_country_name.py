import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_country_name(iso3Code: str, return_original: bool = False)-> dict:
    """Parse country name data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('Country name', {})

    if return_original:
        return test_data


    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        # Field mappings: CIA key -> output key
        field_mappings = {
            'conventional long form': 'country_name_long_form',
            'conventional short form': 'country_name_short_form',
            'local long form': 'country_name_local_long_form',
            'local short form': 'country_name_local_short_form',
            'official long form': 'country_name_official_long_form',
            'official short form': 'country_name_official_short_form',
            'abbreviation': 'country_name_abbreviation',
            'etymology': 'country_name_etymology',
            'former': 'country_name_former',
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

        # Handle note field
        if 'note' in test_data:
            note_data = test_data['note']
            if isinstance(note_data, dict) and 'text' in note_data:
                note_text = note_data['text']
            elif isinstance(note_data, str):
                note_text = note_data
            else:
                note_text = None

            if note_text and note_text.strip():
                result['country_name_note'] = clean_text(note_text)

    except Exception as e:
        logger.error(f"Error parsing country name for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_country_name")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'CHN', 'JPN']:
        print(f"\n{iso3}:")
        try:
            result = parse_country_name(iso3)
            if result:
                print(f"  Long: {result.get('country_name_long_form', 'N/A')}")
                print(f"  Short: {result.get('country_name_short_form', 'N/A')}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
