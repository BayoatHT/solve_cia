import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_06_economy.helper.utils.parse_econ_value import parse_econ_value

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_debt_external(pass_data: dict, iso3Code: str = None) -> dict:
    """Parse debt external from CIA Economy section with separated value components."""
    result = {}
    if not pass_data or not isinstance(pass_data, dict):
        return result
    try:
        yearly_data = []
        for k, v in pass_data.items():
            if k == 'note':
                if isinstance(v, str) and v.strip():
                    result['external_debt_note'] = clean_text(v)
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
            result['external_debt_data'] = yearly_data
            if yearly_data[0].get('value') is not None:
                result['external_debt_latest_value'] = yearly_data[0]['value']
            result['external_debt_latest_year'] = yearly_data[0]['year']
            if yearly_data[0].get('unit'):
                result['external_debt_unit'] = yearly_data[0]['unit']
    except Exception as e:
        logging.error(f"Error parsing debt_external: {e}")
    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 8 >>> 'Debt - external'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Debt - external 2019": {
            "text": "$20,275,951,000,000 (2019 est.)"
        },
        "Debt - external 2018": {
            "text": "$19,452,478,000,000 (2018 est.)"
        },
        "note": "<strong>note:</strong> approximately 4/5ths of US external debt is denominated in US dollars; foreign lenders have been willing to hold US dollar denominated debt instruments because they view the dollar as the world's reserve currency"
    }
    parsed_data = parse_debt_external(pass_data)
    print(parsed_data)
