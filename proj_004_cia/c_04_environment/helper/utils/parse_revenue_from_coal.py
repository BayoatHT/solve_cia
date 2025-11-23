import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_revenue_from_coal(coal_data: dict, iso3Code: str = None) -> dict:
    """Parse revenue from coal data."""
    result = {
        "revenue_coal": {
            "value": None,
            "unit": "% of GDP",
            "timestamp": None,
            "is_estimate": False
        },
        "revenue_coal_note": ""
    }

    if not coal_data or not isinstance(coal_data, dict):
        return result

    text = coal_data.get('text', '')
    if text and text.upper() != 'NA':
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            result['revenue_coal']['value'] = float(pct_match.group(1))

        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            result['revenue_coal']['timestamp'] = year_match.group(1)
            result['revenue_coal']['is_estimate'] = 'est' in text.lower()

    return result


if __name__ == "__main__":
    print(parse_revenue_from_coal({"text": "0.2% of GDP (2018 est.)"}))
