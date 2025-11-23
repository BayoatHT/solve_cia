import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_gdp_official_exchange(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse gdp official exchange from CIA Economy section."""
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
            result['gdp_official_exchange_data'] = yearly_data
            result['gdp_official_exchange_latest'] = yearly_data[0]['value']
            result['gdp_official_exchange_latest_year'] = yearly_data[0]['year']
        if 'text' in pass_data:
            result['gdp_official_exchange'] = clean_text(pass_data['text'])
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['gdp_official_exchange_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing gdp_official_exchange: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 16 >>> 'GDP (official exchange rate)'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "$27.361 trillion (2023 est.)",
        "note": "<b>note:</b> data in current dollars at official exchange rate"
    }
    parsed_data = parse_gdp_official_exchange(pass_data)
    print(parsed_data)
