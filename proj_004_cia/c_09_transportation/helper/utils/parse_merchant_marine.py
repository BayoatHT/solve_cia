"""
Parse merchant marine data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_merchant_marine(merchant_marine_data: dict, iso3Code: str = None) -> dict:
    """
    Parse merchant marine data into structured format.

    Args:
        merchant_marine_data: Dict with subfields: total, by type, note
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - merchant_total_value: int (total ships)
            - merchant_total_year: int
            - merchant_by_type: list of {type, count} dicts
            - merchant_note: str

    Example:
        Input: {"total": {"text": "3,533 (2023)"}, "by type": {"text": "bulk carrier 4, container ship 60"}}
        Output: {
            'merchant_total_value': 3533,
            'merchant_total_year': 2023,
            'merchant_by_type': [{'type': 'bulk carrier', 'count': 4}, {'type': 'container ship', 'count': 60}]
        }
    """
    result = {}

    if not merchant_marine_data:
        return result

    try:
        # Parse total
        if 'total' in merchant_marine_data:
            total_data = merchant_marine_data['total']
            if isinstance(total_data, dict) and 'text' in total_data:
                parsed = parse_transport_value(total_data['text'])
                if parsed['value'] is not None:
                    result['merchant_total_value'] = int(parsed['value'])
                if parsed['year']:
                    result['merchant_total_year'] = parsed['year']

        # Parse by type
        if 'by type' in merchant_marine_data:
            by_type_data = merchant_marine_data['by type']
            if isinstance(by_type_data, dict) and 'text' in by_type_data:
                text = by_type_data['text']
                ship_types = []

                # Pattern: "bulk carrier 4, container ship 60, general cargo 96"
                # Split by comma and parse each segment
                segments = text.split(',')
                for segment in segments:
                    segment = segment.strip()
                    # Match pattern: "type name count"
                    match = re.match(r'(.+?)\s+(\d+)$', segment)
                    if match:
                        ship_type = match.group(1).strip()
                        count = int(match.group(2))
                        ship_types.append({'type': ship_type, 'count': count})

                if ship_types:
                    result['merchant_by_type'] = ship_types

        # Parse note
        if 'note' in merchant_marine_data:
            note = merchant_marine_data['note']
            if note and isinstance(note, str) and note.strip():
                result['merchant_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing merchant_marine for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "total": {"text": "3,533 (2023)"},
        "by type": {"text": "bulk carrier 4, container ship 60, general cargo 96, oil tanker 68, other 3,305"},
        "note": "note - oceangoing self-propelled, cargo-carrying vessels of 1,000 gross tons and above"
    }
    parsed = parse_merchant_marine(test_data, "USA")
    print(parsed)
