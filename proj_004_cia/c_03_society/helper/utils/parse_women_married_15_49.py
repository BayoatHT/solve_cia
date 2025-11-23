import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_women_married_15_49(women_data: dict, iso3Code: str = None) -> dict:
    """
    Parse currently married women (ages 15-49) data from CIA World Factbook format.

    Handles format: "51.9% (2023 est.)"
    """
    result = {
        "women_married_15_49": {
            "value": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "women_married_15_49_note": ""
    }

    if not women_data or not isinstance(women_data, dict):
        return result

    text = women_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    pct_match = re.search(r'([\d.]+)%', text)
    year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)

    if pct_match:
        result["women_married_15_49"]["value"] = float(pct_match.group(1))
    if year_match:
        result["women_married_15_49"]["timestamp"] = year_match.group(1)
        if year_match.group(2):
            result["women_married_15_49"]["is_estimate"] = True

    return result


if __name__ == "__main__":
    test1 = {"text": "51.9% (2023 est.)"}
    print(parse_women_married_15_49(test1))
