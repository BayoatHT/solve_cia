import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_hiv_rate(hiv_data: dict, iso3Code: str = None) -> dict:
    """
    Parse HIV/AIDS adult prevalence rate from CIA World Factbook format.

    Handles format: "1.2% (2021 est.)" or "<0.1% (2021 est.)"
    """
    result = {
        "hiv_prevalence_rate": {
            "value": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False,
            "is_less_than": False
        },
        "hiv_prevalence_rate_note": ""
    }

    if not hiv_data or not isinstance(hiv_data, dict):
        return result

    text = hiv_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    # Check for "<0.1%" pattern
    is_less_than = '<' in text

    pct_match = re.search(r'([\d.]+)%', text)
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

    if pct_match:
        result["hiv_prevalence_rate"]["value"] = float(pct_match.group(1))
        result["hiv_prevalence_rate"]["is_less_than"] = is_less_than
    if year_match:
        result["hiv_prevalence_rate"]["timestamp"] = year_match.group(1)
        if year_match.group(2):
            result["hiv_prevalence_rate"]["is_estimate"] = True

    return result


if __name__ == "__main__":
    test1 = {"text": "1.2% (2021 est.)"}
    print(parse_hiv_rate(test1))
    test2 = {"text": "<0.1% (2021 est.)"}
    print(parse_hiv_rate(test2))
