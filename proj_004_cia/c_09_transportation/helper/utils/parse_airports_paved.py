"""
Parse airports with paved runways from CIA World Factbook (legacy field).
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_airports_paved(airports_paved_data: dict, iso3Code: str = None) -> dict:
    """
    Parse airports with paved runways data (legacy field, only 1 country).

    Args:
        airports_paved_data: Dict with subfields for total and runway lengths
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - paved_runways_total_value: int
            - paved_runways_total_year: int
            - paved_runways_by_length: list of {length_range, count}

    Example:
        Input: {"total": {"text": "3 (2019)"}, "2,438 to 3,047 m": {"text": "3"}}
        Output: {
            'paved_runways_total_value': 3,
            'paved_runways_total_year': 2019,
            'paved_runways_by_length': [{'range': '2,438 to 3,047 m', 'count': 3}]
        }
    """
    result = {}

    if not airports_paved_data:
        return result

    try:
        # Parse total
        if 'total' in airports_paved_data:
            total_data = airports_paved_data['total']
            if isinstance(total_data, dict) and 'text' in total_data:
                parsed = parse_transport_value(total_data['text'])
                if parsed['value'] is not None:
                    result['paved_runways_total_value'] = int(parsed['value'])
                if parsed['year']:
                    result['paved_runways_total_year'] = parsed['year']

        # Parse runway lengths
        by_length = []
        for key, val in airports_paved_data.items():
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
            result['paved_runways_by_length'] = by_length

    except Exception as e:
        logging.error(f"Error parsing airports_paved for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "total": {"text": "3 (2019)"},
        "2,438 to 3,047 m": {"text": "3"}
    }
    parsed = parse_airports_paved(test_data)
    print(parsed)
