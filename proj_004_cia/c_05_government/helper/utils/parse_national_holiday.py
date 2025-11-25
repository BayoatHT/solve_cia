import re
import json
import logging
from typing import Dict, List, Any, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_national_holiday(iso3Code: str, return_original: bool = False)-> dict:
    """Parse national holiday data from CIA Government section for a given country."""
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    government_section = raw_data.get('Government', {})
    test_data = government_section.get('National holiday', {})

    if return_original:
        return test_data


    if not test_data or not isinstance(test_data, dict):
        return result

    try:
        if 'text' in test_data:
            text = test_data['text']
            if text and isinstance(text, str):
                result['national_holiday_description'] = clean_text(text)
                date_match = re.search(r'(\d{1,2}\s+\w+)', text)
                if date_match:
                    result['national_holiday_date'] = date_match.group(1)

        if 'note' in test_data:
            note = test_data['note']
            if isinstance(note, str) and note.strip():
                result['national_holiday_note'] = clean_text(note)

    except Exception as e:
        logger.error(f"Error parsing national holiday for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_national_holiday")
    print("="*60)
    for iso3 in ['USA', 'FRA', 'DEU', 'GBR', 'IND', 'MEX']:
        print(f"\n{iso3}:")
        try:
            result = parse_national_holiday(iso3)
            if result:
                print(f"  Date: {result.get('national_holiday_date', 'N/A')}")
                print(f"  Desc: {result.get('national_holiday_description', 'N/A')[:50]}...")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
