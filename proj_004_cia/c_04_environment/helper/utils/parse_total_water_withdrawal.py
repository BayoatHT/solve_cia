import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_total_water_withdrawal(iso3Code: str) -> dict:
    """Parse total water withdrawal from CIA Environment section for a given country."""
    result = {
        "water_withdrawal": {
            "municipal": None,
            "industrial": None,
            "agricultural": None,
            "unit": "cubic meters",
            "timestamp": None,
            "is_estimate": False
        },
        "water_withdrawal_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    environment_section = raw_data.get('Environment', {})
    withdrawal_data = environment_section.get('Total water withdrawal', {})

    if not withdrawal_data or not isinstance(withdrawal_data, dict):
        return result

    def extract_value(text):
        if not text:
            return None, None, False
        value = None
        year = None
        is_est = False

        num_match = re.search(r'([\d,.]+)\s*(trillion|billion|million)?', text)
        if num_match:
            value = float(num_match.group(1).replace(',', ''))
            mult = num_match.group(2)
            if mult == 'trillion':
                value *= 1e12
            elif mult == 'billion':
                value *= 1e9
            elif mult == 'million':
                value *= 1e6

        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            year = year_match.group(1)
            is_est = 'est' in text.lower()

        return value, year, is_est

    # Parse municipal
    muni = withdrawal_data.get('municipal', {})
    if muni and isinstance(muni, dict):
        text = muni.get('text', '')
        if text and text.upper() != 'NA':
            value, year, is_est = extract_value(text)
            result['water_withdrawal']['municipal'] = value
            result['water_withdrawal']['timestamp'] = year
            result['water_withdrawal']['is_estimate'] = is_est

    # Parse industrial
    ind = withdrawal_data.get('industrial', {})
    if ind and isinstance(ind, dict):
        text = ind.get('text', '')
        if text and text.upper() != 'NA':
            value, _, _ = extract_value(text)
            result['water_withdrawal']['industrial'] = value

    # Parse agricultural
    ag = withdrawal_data.get('agricultural', {})
    if ag and isinstance(ag, dict):
        text = ag.get('text', '')
        if text and text.upper() != 'NA':
            value, _, _ = extract_value(text)
            result['water_withdrawal']['agricultural'] = value

    note = withdrawal_data.get('note', '')
    if note:
        result['water_withdrawal_note'] = clean_text(note)

    return result


if __name__ == "__main__":
    print("="*60)
    print("Testing parse_total_water_withdrawal")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'DEU']:
        print(f"\n{iso3}:")
        try:
            result = parse_total_water_withdrawal(iso3)
            if result and result['water_withdrawal']['municipal']:
                ww = result['water_withdrawal']
                muni = ww['municipal'] / 1e9 if ww['municipal'] else 0
                ind = ww['industrial'] / 1e9 if ww['industrial'] else 0
                ag = ww['agricultural'] / 1e9 if ww['agricultural'] else 0
                print(f"  Municipal: {muni:,.1f} billion m³")
                print(f"  Industrial: {ind:,.1f} billion m³")
                print(f"  Agricultural: {ag:,.1f} billion m³")
                print(f"  Year: {ww['timestamp']}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
