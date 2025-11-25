import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_env_international_agreements(iso3Code: str, return_original: bool = False)-> dict:
    """Parse environment international agreements from CIA Environment section for a given country."""
    result = {
        "international_agreements": {
            "party_to": [],
            "signed_not_ratified": []
        },
        "international_agreements_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    agreements_data = environment_section.get('Environment - international agreements', {})

    if return_original:
        return agreements_data


    if not agreements_data or not isinstance(agreements_data, dict):
        return result

    # Parse party to
    party_data = agreements_data.get('party to', {})
    if party_data and isinstance(party_data, dict):
        text = party_data.get('text', '')
        if text and text.upper() != 'NA':
            # Split by comma and clean
            agreements = [a.strip() for a in text.split(',') if a.strip()]
            result['international_agreements']['party_to'] = agreements

    # Parse signed but not ratified
    signed_data = agreements_data.get('signed, but not ratified', {})
    if signed_data and isinstance(signed_data, dict):
        text = signed_data.get('text', '')
        if text and text.upper() != 'NA':
            agreements = [a.strip() for a in text.split(',') if a.strip()]
            result['international_agreements']['signed_not_ratified'] = agreements

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_env_international_agreements")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'DEU']:
        print(f"\n{iso3}:")
        try:
            result = parse_env_international_agreements(iso3)
            if result and result['international_agreements']['party_to']:
                party = result['international_agreements']['party_to']
                signed = result['international_agreements']['signed_not_ratified']
                print(f"  Party to: {len(party)} agreements")
                print(f"  Signed not ratified: {len(signed)} agreements")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
