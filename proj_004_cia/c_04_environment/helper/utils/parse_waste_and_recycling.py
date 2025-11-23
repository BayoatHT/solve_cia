import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_waste_and_recycling(waste_data: dict, iso3Code: str = None) -> dict:
    """Parse waste and recycling data."""
    result = {
        "waste_recycling": {
            "waste_generated": None,
            "waste_generated_unit": "tons",
            "waste_recycled": None,
            "waste_recycled_unit": "tons",
            "recycling_percent": None,
            "timestamp": None,
            "is_estimate": False
        },
        "waste_recycling_note": ""
    }

    if not waste_data or not isinstance(waste_data, dict):
        return result

    def extract_value_and_year(text):
        if not text:
            return None, None, False
        value = None
        year = None
        is_est = False

        # Extract number with units like "258 million tons"
        num_match = re.search(r'([\d,.]+)\s*(million|billion|thousand)?', text)
        if num_match:
            value = float(num_match.group(1).replace(',', ''))
            multiplier = num_match.group(2)
            if multiplier == 'million':
                value *= 1_000_000
            elif multiplier == 'billion':
                value *= 1_000_000_000
            elif multiplier == 'thousand':
                value *= 1_000

        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            year = year_match.group(1)
            is_est = 'est' in text.lower()

        return value, year, is_est

    # Parse waste generated
    gen_data = waste_data.get('municipal solid waste generated annually', {})
    if gen_data and isinstance(gen_data, dict):
        text = gen_data.get('text', '')
        if text and text.upper() != 'NA':
            value, year, is_est = extract_value_and_year(text)
            result['waste_recycling']['waste_generated'] = value
            result['waste_recycling']['timestamp'] = year
            result['waste_recycling']['is_estimate'] = is_est

    # Parse waste recycled
    rec_data = waste_data.get('municipal solid waste recycled annually', {})
    if rec_data and isinstance(rec_data, dict):
        text = rec_data.get('text', '')
        if text and text.upper() != 'NA':
            value, _, _ = extract_value_and_year(text)
            result['waste_recycling']['waste_recycled'] = value

    # Parse recycling percentage
    pct_data = waste_data.get('percent of municipal solid waste recycled', {})
    if pct_data and isinstance(pct_data, dict):
        text = pct_data.get('text', '')
        if text and text.upper() != 'NA':
            pct_match = re.search(r'([\d.]+)%', text)
            if pct_match:
                result['waste_recycling']['recycling_percent'] = float(pct_match.group(1))

    return result


if __name__ == "__main__":
    test_data = {
        "municipal solid waste generated annually": {"text": "258 million tons (2015 est.)"},
        "percent of municipal solid waste recycled": {"text": "34.6% (2014 est.)"}
    }
    print(parse_waste_and_recycling(test_data))
