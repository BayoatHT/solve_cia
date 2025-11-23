import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_exports(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse exports from CIA Economy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['exports_note'] = clean_text(v)
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
            result['exports_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['exports_latest_value'] = yearly_data[0]['value']
            result['exports_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['exports_unit'] = yearly_data[0]['unit']
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
