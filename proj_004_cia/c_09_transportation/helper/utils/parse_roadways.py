"""
Parse roadways data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_roadways(roadways_data: dict, iso3Code: str = None) -> dict:
    """
    Parse roadways data into structured format.

    Args:
        roadways_data: Dict with subfields: total, paved, unpaved, urban, non-urban, etc.
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - roadways_total_value: float (total km)
            - roadways_total_year: int
            - roadways_paved_value: float (paved km)
            - roadways_unpaved_value: float (unpaved km)
            - roadways_urban_value: float (urban km)
            - roadways_expressways_km: float (if mentioned)
            - roadways_note: str

    Example:
        Input: {"total": {"text": "6,586,610 km"}, "paved": {"text": "4,304,715 km (includes 76,334 km of expressways)"}}
        Output: {'roadways_total_value': 6586610.0, 'roadways_paved_value': 4304715.0, 'roadways_expressways_km': 76334.0}
    """
    result = {}

    if not roadways_data:
        return result

    try:
        # Field mapping: CIA field name -> output prefix
        field_mappings = {
            'total': 'roadways_total',
            'paved': 'roadways_paved',
            'unpaved': 'roadways_unpaved',
            'urban': 'roadways_urban',
            'non-urban': 'roadways_non_urban',
            'non urban': 'roadways_non_urban',
            'private and forest roads': 'roadways_private_forest',
            'Turkish Cypriot control': 'roadways_turkish_cypriot',
        }

        for cia_field, output_prefix in field_mappings.items():
            if cia_field in roadways_data:
                field_data = roadways_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    parsed = parse_transport_value(text)

                    if parsed['value'] is not None:
                        result[f'{output_prefix}_value'] = parsed['value']
                    if parsed['unit']:
                        result[f'{output_prefix}_unit'] = parsed['unit']
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']

                    # Extract expressways km if present (e.g., "includes 76,334 km of expressways")
                    if cia_field == 'paved':
                        expressway_match = re.search(r'([\d,]+)\s*km\s*(?:of\s*)?expressways?', text)
                        if expressway_match:
                            expressway_km = float(expressway_match.group(1).replace(',', ''))
                            result['roadways_expressways_km'] = expressway_km

        # Parse note
        if 'note' in roadways_data:
            note = roadways_data['note']
            if note and isinstance(note, str) and note.strip():
                result['roadways_note'] = clean_text(note)

    except Exception as e:
        logging.error(f"Error parsing roadways for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "total": {"text": "6,586,610 km"},
        "paved": {"text": "4,304,715 km (includes 76,334 km of expressways)"},
        "unpaved": {"text": "2,281,895 km (2012)"}
    }
    parsed = parse_roadways(test_data, "USA")
    print(parsed)
