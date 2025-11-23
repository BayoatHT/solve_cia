"""
Parse railways data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_railways(railways_data: dict, iso3Code: str = None) -> dict:
    """
    Parse railways data into structured format.

    Args:
        railways_data: Dict with subfields: total, broad gauge, standard gauge,
                      narrow gauge, dual gauge, note
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - railways_total_value: float (total km)
            - railways_total_year: int
            - railways_standard_value: float (standard gauge km)
            - railways_standard_gauge: str (gauge width e.g. "1.435-m")
            - railways_broad_value: float (broad gauge km)
            - railways_narrow_value: float (narrow gauge km)
            - railways_dual_value: float (dual gauge km)
            - railways_note: str

    Example:
        Input: {"total": {"text": "293,564.2 km (2014)"}, "standard gauge": {...}}
        Output: {'railways_total_value': 293564.2, 'railways_total_year': 2014, ...}
    """
    result = {}

    if not railways_data:
        return result

    try:
        # Field mapping: CIA field name -> output prefix
        field_mappings = {
            'total': 'railways_total',
            'standard gauge': 'railways_standard',
            'broad gauge': 'railways_broad',
            'narrow gauge': 'railways_narrow',
            'dual gauge': 'railways_dual',
        }

        for cia_field, output_prefix in field_mappings.items():
            if cia_field in railways_data:
                field_data = railways_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    parsed = parse_transport_value(text)

                    if parsed['value'] is not None:
                        result[f'{output_prefix}_value'] = parsed['value']
                    if parsed['unit']:
                        result[f'{output_prefix}_unit'] = parsed['unit']
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']

                    # Extract gauge width (e.g., "1.435-m gauge" or "1.000-m gauge")
                    gauge_match = re.search(r'(\d+\.\d+)-?m(?:\s*gauge)?', text)
                    if gauge_match:
                        result[f'{output_prefix}_gauge_m'] = float(gauge_match.group(1))

                    # Extract electrified km if present
                    electrified_match = re.search(r'([\d,]+)\s*km\s*electrified', text)
                    if electrified_match:
                        electrified_km = float(electrified_match.group(1).replace(',', ''))
                        result[f'{output_prefix}_electrified_km'] = electrified_km

        # Parse note
        if 'note' in railways_data:
            note = railways_data['note']
            if note and isinstance(note, str) and note.strip():
                result['railways_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing railways for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "total": {"text": "293,564.2 km (2014)"},
        "standard gauge": {"text": "293,564.2 km (2014) 1.435-m gauge"},
        "narrow gauge": {"text": "438 km (2014) 1.000-m gauge"},
        "note": "22,207 km 1.067-mm gauge (15,430 km electrified)"
    }
    parsed = parse_railways(test_data, "USA")
    print(parsed)
