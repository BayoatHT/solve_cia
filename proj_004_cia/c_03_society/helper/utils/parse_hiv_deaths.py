import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_hiv_deaths(hiv_data: dict, iso3Code: str = None) -> dict:
    """
    Parse HIV/AIDS deaths from CIA World Factbook format.

    Handles format: "1,200 (2021 est.)" or "<100 (2021 est.)"
    """
    result = {
        "hiv_deaths": {
            "value": None,
            "timestamp": None,
            "is_estimate": False,
            "is_less_than": False
        },
        "hiv_deaths_note": ""
    }

    if not hiv_data or not isinstance(hiv_data, dict):
        return result

    text = hiv_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    # Check for "<100" pattern
    is_less_than = '<' in text

    # Match numbers with commas
    num_match = re.search(r'([\d,]+)', text)
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

    if num_match:
        value_str = num_match.group(1).replace(',', '')
        result["hiv_deaths"]["value"] = int(value_str)
        result["hiv_deaths"]["is_less_than"] = is_less_than
    if year_match:
        result["hiv_deaths"]["timestamp"] = year_match.group(1)
        if year_match.group(2):
            result["hiv_deaths"]["is_estimate"] = True

    return result


if __name__ == "__main__":
    test1 = {"text": "1,200 (2021 est.)"}
    print(parse_hiv_deaths(test1))
    test2 = {"text": "<100 (2021 est.)"}
    print(parse_hiv_deaths(test2))
