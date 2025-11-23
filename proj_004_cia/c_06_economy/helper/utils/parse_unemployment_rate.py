import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_unemployment_rate(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """Parse unemployment rate from CIA Economy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['unemployment_note'] = clean_text(v)
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
            result['unemployment_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['unemployment_latest_value'] = yearly_data[0]['value']
            result['unemployment_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['unemployment_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logging.error(f"Error parsing unemployment_rate: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Unemployment rate 2014" - 'unemploy_rate_2014'
    # "Unemployment rate 2015" - 'unemploy_rate_2015'
    # "Unemployment rate 2016" - 'unemploy_rate_2016'
    # "Unemployment rate 2017" - 'unemploy_rate_2017'
    # "Unemployment rate 2018" - 'unemploy_rate_2018'
    # "Unemployment rate 2019" - 'unemploy_rate_2019'
    # "Unemployment rate 2020" - 'unemploy_rate_2020'
    # "Unemployment rate 2021" - 'unemploy_rate_2021'
    # "Unemployment rate 2022" - 'unemploy_rate_2022'
    # "Unemployment rate 2023" - 'unemploy_rate_2023'
    # "note" - 'unemploy_rate_note'
    # --------------------------------------------------------------------------------------------------
    # ['unemploy_rate_2014', 'unemploy_rate_2015', 'unemploy_rate_2016', 'unemploy_rate_2017',
    # 'unemploy_rate_2018', 'unemploy_rate_2019', 'unemploy_rate_2020', 'unemploy_rate_2021',
    # 'unemploy_rate_2022', 'unemploy_rate_2023', 'unemploy_rate_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Unemployment rate 2023": {
            "text": "23.38% (2023 est.)"
        },
        "Unemployment rate 2022": {
            "text": "23.62% (2022 est.)"
        },
        "Unemployment rate 2021": {
            "text": "23.11% (2021 est.)"
        },
        "note": "<b>note:</b> % of labor force seeking employment"
    }
    parsed_data = parse_unemployment_rate(pass_data)
    print(parsed_data)
