import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_inflation_rate(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse inflation rate from CIA Economy section."""
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
            result['inflation_rate_data'] = yearly_data
            result['inflation_rate_latest'] = yearly_data[0]['value']
            result['inflation_rate_latest_year'] = yearly_data[0]['year']
        if 'text' in pass_data:
            result['inflation_rate'] = clean_text(pass_data['text'])
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['inflation_rate_note'] = clean_text(note)
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
