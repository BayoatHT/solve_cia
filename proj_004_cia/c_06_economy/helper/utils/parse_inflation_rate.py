import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_inflation_rate(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse inflation rate from CIA Economy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['inflation_note'] = clean_text(v)
                continue
            if isinstance(v, dict) and 'text' in v:
                year_match = re.search(r'(\d{4})', k)
                if year_match:
                    year = int(year_match.group(1))
                    text = v.get('text', '')
                    if text:
                        parsed = parse_econ_value(text)
                        entry = {'year': year}
                        if parsed['value'] is not None:
                            entry['value'] = parsed['value']
                        if parsed['unit']:
                            entry['unit'] = parsed['unit']
                        if parsed['is_estimate']:
                            entry['is_estimate'] = parsed['is_estimate']
                        yearly_data.append(entry)
        if yearly_data:
            yearly_data.sort(key=lambda x: x['year'], reverse=True)
            result['inflation_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['inflation_latest_value'] = yearly_data[0]['value']
            result['inflation_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['inflation_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logging.error(f"Error parsing inflation_rate: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 29 >>> 'Inflation rate (consumer prices)'
    # --------------------------------------------------------------------------------------------------
    # GET FROM WORLD BANK
    # "Inflation rate (consumer prices) 2023" - 'inflation_rate_2023'
    # "note" - 'inflation_rate_note'
    # --------------------------------------------------------------------------------------------------
    # ['inflation_rate_2023', 'inflation_rate_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Inflation rate (consumer prices) 2023": {
            "text": "4.12% (2023 est.)"
        },
        "Inflation rate (consumer prices) 2022": {
            "text": "8% (2022 est.)"
        },
        "Inflation rate (consumer prices) 2021": {
            "text": "4.7% (2021 est.)"
        },
        "note": "<b>note:</b> annual % change based on consumer prices"
    }
    parsed_data = parse_inflation_rate(pass_data)
    print(parsed_data)
