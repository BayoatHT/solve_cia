import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_total_renewable_water(iso3Code: str, return_original: bool = False)-> dict:
    """Parse total renewable water resources from CIA Environment section for a given country."""
    result = {
        "renewable_water": {
            "value": None,
            "unit": "cubic meters",
            "timestamp": None,
            "is_estimate": False
        },
        "renewable_water_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    water_data = environment_section.get('Total renewable water resources', {})

    if return_original:
        return water_data


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
    print("="*60)
    print("Testing parse_total_renewable_water")
    print("="*60)
    for iso3 in ['USA', 'BRA', 'RUS', 'CHN', 'IND', 'DEU']:
        print(f"\n{iso3}:")
        try:
            result = parse_total_renewable_water(iso3)
            if result and result['renewable_water']['value']:
                rw = result['renewable_water']
                # Format in billions for readability
                value_billion = rw['value'] / 1e9
                print(f"  Value: {value_billion:,.1f} billion cubic meters")
                print(f"  Year: {rw['timestamp']}, Estimate: {rw['is_estimate']}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
