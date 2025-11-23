"""
Parse airports with unpaved runways from CIA World Factbook (legacy field).
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_airports_unpaved(airports_unpaved_data: dict, iso3Code: str = None) -> dict:
    """
    Parse airports with unpaved runways data (legacy field, only 1 country).

    Args:
        airports_unpaved_data: Dict with subfields for total and runway lengths
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - unpaved_runways_total_value: int
            - unpaved_runways_total_year: int
            - unpaved_runways_by_length: list of {length_range, count}

    Example:
        Input: {"total": {"text": "3 (2013)"}, "914 to 1,523 m": {"text": "1"}}
        Output: {
            'unpaved_runways_total_value': 3,
            'unpaved_runways_total_year': 2013,
            'unpaved_runways_by_length': [{'range': '914 to 1,523 m', 'count': 1}]
        }
    """
    result = {}

    if not airports_unpaved_data:
        return result

    try:
        # Parse total
        if 'total' in airports_unpaved_data:
            total_data = airports_unpaved_data['total']
            if isinstance(total_data, dict) and 'text' in total_data:
                parsed = parse_transport_value(total_data['text'])
                if parsed['value'] is not None:
                    result['unpaved_runways_total_value'] = int(parsed['value'])
                if parsed['year']:
                    result['unpaved_runways_total_year'] = parsed['year']

        # Parse runway lengths
        by_length = []
        for key, val in airports_unpaved_data.items():
            if key == 'total':
                continue
            if isinstance(val, dict) and 'text' in val:
                parsed = parse_transport_value(val['text'])
                if parsed['value'] is not None:
                    by_length.append({
                        'range': key,
                        'count': int(parsed['value'])
                    })

        if by_length:
            result['unpaved_runways_by_length'] = by_length

    except Exception as e:
        logging.error(f"Error parsing airports_unpaved for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "total": {"text": "3 (2013)"},
        "1,524 to 2,437 m": {"text": "1 (2013)"},
        "914 to 1,523 m": {"text": "1 (2013)"},
        "under 914 m": {"text": "1 (2013)"}
    }
    parsed = parse_airports_unpaved(test_data)
    print(parsed)
