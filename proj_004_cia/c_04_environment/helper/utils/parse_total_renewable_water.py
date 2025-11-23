import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_total_renewable_water(water_data: dict, iso3Code: str = None) -> dict:
    """Parse total renewable water resources data."""
    result = {
        "renewable_water": {
            "value": None,
            "unit": "cubic meters",
            "timestamp": None,
            "is_estimate": False
        },
        "renewable_water_note": ""
    }

    if not water_data or not isinstance(water_data, dict):
        return result

    text = water_data.get('text', '')
    if text and text.upper() != 'NA':
        # Extract number with unit multiplier
        num_match = re.search(r'([\d,.]+)\s*(trillion|billion|million)?', text)
        if num_match:
            value = float(num_match.group(1).replace(',', ''))
            multiplier = num_match.group(2)
            if multiplier == 'trillion':
                value *= 1e12
            elif multiplier == 'billion':
                value *= 1e9
            elif multiplier == 'million':
                value *= 1e6
            result['renewable_water']['value'] = value

        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            result['renewable_water']['timestamp'] = year_match.group(1)
            result['renewable_water']['is_estimate'] = 'est' in text.lower()

    note = water_data.get('note', '')
    if note:
        result['renewable_water_note'] = clean_text(note)

    return result


if __name__ == "__main__":
    print(parse_total_renewable_water({"text": "3.07 trillion cubic meters (2020 est.)"}))
