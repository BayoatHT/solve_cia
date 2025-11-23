import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_total_water_withdrawal(withdrawal_data: dict, iso3Code: str = None) -> dict:
    """Parse total water withdrawal data."""
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
    test_data = {
        "municipal": {"text": "58.39 billion cubic meters (2020 est.)"},
        "industrial": {"text": "209.7 billion cubic meters (2020 est.)"},
        "agricultural": {"text": "176.2 billion cubic meters (2020 est.)"}
    }
    print(parse_total_water_withdrawal(test_data))
