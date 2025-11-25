import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_international(iso3Code: str) -> dict:
    """
    Parse international disputes data from CIA Transnational Issues section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary containing parsed information for international disputes and notes.
    """
    result = {
        "international": [],
        "international_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    issues_section = raw_data.get('Transnational Issues', {})
    international_data = issues_section.get('Disputes - international', {})

    if not international_data or not isinstance(international_data, dict):
        return result

    try:
        # Handle main 'text'
        international_text = international_data.get("text", "")
        if international_text:
            result["international"] = parse_text_to_list(international_text)

        # Handle 'note'
        international_note = international_data.get("note", "")
        if international_note:
            result["international_note"] = clean_text(international_note)

    except Exception as e:
        logger.error(f"Error parsing international for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_international")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'IND', 'JPN', 'ISR']:
        print(f"\n{iso3}:")
        try:
            result = parse_international(iso3)
            if result.get('international'):
                disputes = result['international']
                print(f"  Disputes: {len(disputes)}")
                if disputes:
                    print(f"    First: {str(disputes[0])[:50]}...")
            else:
                print("  No international disputes data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
