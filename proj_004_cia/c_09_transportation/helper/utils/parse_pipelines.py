"""
Parse pipelines data from CIA World Factbook Transportation section.
"""
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_09_transportation.helper.utils.parse_transport_value import parse_pipeline_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_pipelines(pipelines_data: dict, iso3Code: str = None) -> dict:
    """
    Parse pipelines data into structured format.

    Args:
        pipelines_data: Dict with 'text' containing pipeline info
        iso3Code: Country ISO3 code

    Returns:
        Dict with:
            - pipelines_data: list of pipeline segments with value, unit, type
            - pipelines_total_km: float (total km of all pipelines)
            - pipelines_year: int (data year)

    Example:
        Input: {"text": "1,984,321 km natural gas, 240,711 km petroleum products (2013)"}
        Output: {
            'pipelines_data': [
                {'value': 1984321.0, 'unit': 'km', 'type': 'natural gas'},
                {'value': 240711.0, 'unit': 'km', 'type': 'petroleum products'}
            ],
            'pipelines_total_km': 2225032.0,
            'pipelines_year': 2013
        }
    """
    result = {}

    if not pipelines_data:
        return result

    try:
        if 'text' in pipelines_data:
            text = pipelines_data['text']
            pipelines = parse_pipeline_text(text)

            if pipelines:
                result['pipelines_data'] = pipelines

                # Calculate total km
                total_km = sum(p.get('value', 0) for p in pipelines if p.get('unit') == 'km')
                if total_km > 0:
                    result['pipelines_total_km'] = total_km

                # Extract year from first pipeline entry
                if pipelines[0].get('year'):
                    result['pipelines_year'] = pipelines[0]['year']

    except Exception as e:
        logging.error(f"Error parsing pipelines for {iso3Code}: {e}")

    return result


# Example usage
if __name__ == "__main__":
    test_data = {
        "text": "1,984,321 km natural gas, 240,711 km petroleum products (2013)"
    }
    parsed = parse_pipelines(test_data, "USA")
    print(parsed)
