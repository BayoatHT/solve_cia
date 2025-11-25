import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_real_gdp_ppp(iso3Code: str, return_original: bool = False)-> dict:
    """Parse Real GDP (purchasing power parity) from CIA World Factbook."""
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result
    
    economy_section = raw_data.get('Economy', {})
    pass_data = economy_section.get('Real GDP (purchasing power parity)', {})

    if return_original:
        return pass_data

    if not pass_data or not isinstance(pass_data, dict):
        return result
    
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['gdp_ppp_note'] = clean_text(v)
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
            result['gdp_ppp_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['gdp_ppp_latest_value'] = yearly_data[0]['value']
            result['gdp_ppp_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['gdp_ppp_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logger.error(f"Error parsing real_gdp_ppp for {iso3Code}: {e}")
    return result

if __name__ == "__main__":
    print("Testing parse_real_gdp_ppp")
    for iso3 in ['USA', 'CHN', 'DEU']:
        result = parse_real_gdp_ppp(iso3)
        print(f"{iso3}: {result.get('gdp_ppp_latest_value', 'No data')}")
