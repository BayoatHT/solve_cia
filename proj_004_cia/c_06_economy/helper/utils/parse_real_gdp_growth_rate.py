import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_real_gdp_growth_rate(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse real gdp growth rate from CIA Economy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['gdp_growth_note'] = clean_text(v)
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
            result['gdp_growth_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['gdp_growth_latest_value'] = yearly_data[0]['value']
            result['gdp_growth_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['gdp_growth_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logging.error(f"Error parsing real_gdp_growth_rate: {e}")
    return result
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if isinstance(v, dict) and 'text' in v:
                year_match = re.search(r'(\d{4})', k)
                if year_match:
                    year = int(year_match.group(1))
                    text = v.get('text', '')
                    if text:
                        yearly_data.append({'year': year, 'value': clean_text(text)})
        if yearly_data:
            yearly_data.sort(key=lambda x: x['year'], reverse=True)
            result['real_gdp_growth_rate_data'] = yearly_data
            result['real_gdp_growth_rate_latest'] = yearly_data[0]['value']
            result['real_gdp_growth_rate_latest_year'] = yearly_data[0]['year']
        if 'text' in pass_data:
            result['real_gdp_growth_rate'] = clean_text(pass_data['text'])
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['real_gdp_growth_rate_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing real_gdp_growth_rate: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 35 >>> 'Real GDP growth rate'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Real GDP growth rate 2023": {
            "text": "2.73% (2023 est.)"
        },
        "Real GDP growth rate 2022": {
            "text": "5.49% (2022 est.)"
        },
        "Real GDP growth rate 2021": {
            "text": "11.92% (2021 est.)"
        },
        "note": "<b>note:</b> annual GDP % growth based on constant local currency"
    }
    parsed_data = parse_real_gdp_growth_rate(pass_data)
    print(parsed_data)
