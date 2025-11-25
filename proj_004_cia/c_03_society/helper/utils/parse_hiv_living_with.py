import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_hiv_living_with(hiv_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse HIV/AIDS people living with HIV/AIDS from CIA World Factbook format.

    Handles format: "1.2 million (2021 est.)" or "150,000 (2021 est.)"
    """
    if return_original:
        return hiv_data

    result = {
        "hiv_living_with": {
            "value": None,
            "timestamp": None,
            "is_estimate": False,
            "is_less_than": False
        },
        "hiv_living_with_note": ""
    }

    if not hiv_data or not isinstance(hiv_data, dict):
        return result

    text = hiv_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    is_less_than = '<' in text

    # Match "1.2 million" or plain numbers with commas
    million_match = re.search(r'([\d.]+)\s*million', text, re.IGNORECASE)
    num_match = re.search(r'([\d,]+)', text)
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

    if million_match:
        result["hiv_living_with"]["value"] = int(float(million_match.group(1)) * 1_000_000)
        result["hiv_living_with"]["is_less_than"] = is_less_than
    elif num_match:
        value_str = num_match.group(1).replace(',', '')
        result["hiv_living_with"]["value"] = int(value_str)
        result["hiv_living_with"]["is_less_than"] = is_less_than

    if year_match:
        result["hiv_living_with"]["timestamp"] = year_match.group(1)
        if year_match.group(2):
            result["hiv_living_with"]["is_estimate"] = True

    return result


if __name__ == "__main__":
    test1 = {"text": "1.2 million (2021 est.)"}
    print(parse_hiv_living_with(test1))
    test2 = {"text": "150,000 (2021 est.)"}
    print(parse_hiv_living_with(test2))
