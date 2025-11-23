import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_exports(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse exports from CIA Economy section."""
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
            result['exports_data'] = yearly_data
            result['exports_latest'] = yearly_data[0]['value']
            result['exports_latest_year'] = yearly_data[0]['year']
        if 'text' in pass_data:
            result['exports'] = clean_text(pass_data['text'])
        if 'note' in pass_data:
            note = pass_data['note']
            if isinstance(note, str) and note.strip():
                result['exports_note'] = clean_text(note)
    except Exception as e:
        logging.error(f"Error parsing exports: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 12 >>> 'Exports'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Exports 2023": {
            "text": "$3.052 trillion (2023 est.)"
        },
        "Exports 2022": {
            "text": "$3.018 trillion (2022 est.)"
        },
        "Exports 2021": {
            "text": "$2.567 trillion (2021 est.)"
        },
        "note": "<strong>note:</strong> balance of payments - exports of goods and services in current dollars"
    }
    parsed_data = parse_exports(pass_data)
    print(parsed_data)
