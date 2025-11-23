import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_gdp_per_capita_ppp(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse gdp per capita ppp from CIA Economy section."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
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
            result['gdp_per_capita_ppp_data'] = yearly_data
            result['gdp_per_capita_ppp_latest'] = yearly_data[0]['value']
            result['gdp_per_capita_ppp_latest_year'] = yearly_data[0]['year']
        if 'text' in pass_data:
            result['gdp_per_capita_ppp'] = clean_text(pass_data['text'])
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['gdp_per_capita_ppp_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing gdp_per_capita_ppp: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 20 >>> 'GDP - per capita (PPP)'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "$2,500 (2007 est.)"
    }
    parsed_data = parse_gdp_per_capita_ppp(pass_data)
    print(parsed_data)
