"""
Parse ports data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ports(ports_data: dict, iso3Code: str = None) -> dict:
    """
    Parse ports data into structured format.

    Args:
        ports_data: Dict with subfields: total ports, large, medium, small, very small,
                   ports with oil terminals, key ports
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - ports_total_value: int (total ports)
            - ports_total_year: int
            - ports_large_value: int
            - ports_medium_value: int
            - ports_small_value: int
            - ports_very_small_value: int
            - ports_oil_terminals_value: int
            - ports_key_list: list of port names

    Example:
        Input: {"total ports": {"text": "666 (2024)"}, "large": {"text": "21"}}
        Output: {'ports_total_value': 666, 'ports_total_year': 2024, 'ports_large_value': 21}
    """
    result = {}

    if not ports_data:
        return result

    try:
        # Field mapping: CIA field name -> output prefix
        field_mappings = {
            'total ports': 'ports_total',
            'large': 'ports_large',
            'medium': 'ports_medium',
            'small': 'ports_small',
            'very small': 'ports_very_small',
            'ports with oil terminals': 'ports_oil_terminals',
            'size unknown': 'ports_size_unknown',
        }

        for cia_field, output_prefix in field_mappings.items():
            if cia_field in ports_data:
                field_data = ports_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    parsed = parse_transport_value(field_data['text'])
                    if parsed['value'] is not None:
                        result[f'{output_prefix}_value'] = int(parsed['value'])
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']

        # Parse key ports list
        if 'key ports' in ports_data:
            key_ports_data = ports_data['key ports']
            if isinstance(key_ports_data, dict) and 'text' in key_ports_data:
                text = key_ports_data['text']
                # Split by comma and clean
                ports_list = [clean_text(p.strip()) for p in text.split(',') if p.strip()]
                if ports_list:
                    result['ports_key_list'] = ports_list

    except Exception as e:
        logging.error(f"Error parsing ports for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "total ports": {"text": "666 (2024)"},
        "large": {"text": "21"},
        "medium": {"text": "38"},
        "small": {"text": "132"},
        "very small": {"text": "475"},
        "ports with oil terminals": {"text": "204"},
        "key ports": {"text": "Baltimore, Boston, Brooklyn, Los Angeles, New York City"}
    }
    parsed = parse_ports(test_data, "USA")
    print(parsed)
