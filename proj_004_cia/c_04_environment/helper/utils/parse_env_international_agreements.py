import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_env_international_agreements(agreements_data: dict, iso3Code: str = None) -> dict:
    """Parse environment international agreements data."""
    result = {
        "international_agreements": {
            "party_to": [],
            "signed_not_ratified": []
        },
        "international_agreements_note": ""
    }

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
    test_data = {
        "party to": {"text": "Climate Change, Biodiversity, Desertification"},
        "signed, but not ratified": {"text": "Hazardous Wastes"}
    }
    print(parse_env_international_agreements(test_data))
