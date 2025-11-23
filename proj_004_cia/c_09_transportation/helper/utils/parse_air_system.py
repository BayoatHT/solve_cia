"""
Parse national air transport system data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_transport_value

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_air_system(air_system_data: dict, iso3Code: str = None) -> dict:
    """
    Parse national air transport system data into structured format.

    Args:
        air_system_data: Dict with subfields for carriers, aircraft, passengers, freight
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - air_carriers_value: int (number of registered air carriers)
            - air_carriers_year: int
            - air_aircraft_value: int (inventory of registered aircraft)
            - air_passengers_value: float (annual passenger traffic)
            - air_passengers_year: int
            - air_freight_value: float (annual freight in mt-km)
            - air_freight_unit: str (e.g., "mt-km")
            - air_freight_year: int

    Example:
        Input: {"number of registered air carriers": {"text": "99 (2020)"}}
        Output: {'air_carriers_value': 99, 'air_carriers_year': 2020}
    """
    result = {}

    if not air_system_data:
        return result

    try:
        # Field mapping: CIA field name -> output prefix
        field_mappings = {
            'number of registered air carriers': 'air_carriers',
            'inventory of registered aircraft operated by air carriers': 'air_aircraft',
            'annual passenger traffic on registered air carriers': 'air_passengers',
            'annual freight traffic on registered air carriers': 'air_freight',
        }

        for cia_field, output_prefix in field_mappings.items():
            if cia_field in air_system_data:
                field_data = air_system_data[cia_field]
                if isinstance(field_data, dict) and 'text' in field_data:
                    text = field_data['text']
                    parsed = parse_transport_value(text)

                    if parsed['value'] is not None:
                        # For carriers and aircraft, use int; for passengers/freight, use float
                        if output_prefix in ['air_carriers', 'air_aircraft']:
                            result[f'{output_prefix}_value'] = int(parsed['value'])
                        else:
                            result[f'{output_prefix}_value'] = parsed['value']

                    if parsed['unit']:
                        result[f'{output_prefix}_unit'] = parsed['unit']
                    if parsed['year']:
                        result[f'{output_prefix}_year'] = parsed['year']
                    if parsed['magnitude']:
                        result[f'{output_prefix}_magnitude'] = parsed['magnitude']

    except Exception as e:
        logging.error(f"Error parsing air_system for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "number of registered air carriers": {"text": "99 (2020)"},
        "inventory of registered aircraft operated by air carriers": {"text": "7,249"},
        "annual passenger traffic on registered air carriers": {"text": "889.022 million (2018)"},
        "annual freight traffic on registered air carriers": {"text": "42,985,300,000 mt-km (2018)"}
    }
    parsed = parse_air_system(test_data, "USA")
    print(parsed)
