import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_mothers_age_at_first_birth(mothers_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse mother's mean age at first birth from CIA World Factbook format.

    Handles formats:
    1. Standard: "31.1 years (2020 est.)"
    2. NA values
    """
    if return_original:
        return mothers_data

    result = {
        "mothers_mean_age_first_birth": {
            "value": None,
            "unit": "years",
            "timestamp": None,
            "is_estimate": False
        },
        "mothers_mean_age_first_birth_note": ""
    }

    if not mothers_data or not isinstance(mothers_data, dict):
        return result

    text = mothers_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    PATTERN = re.compile(r'([\d.]+)\s*years?\s*(?:\(([\d]{4})\s*(est\.?)?\))?')
    match = PATTERN.search(text)
    if match:
        result["mothers_mean_age_first_birth"]["value"] = float(match.group(1))
        if match.group(2):
            result["mothers_mean_age_first_birth"]["timestamp"] = match.group(2)
        if match.group(3):
            result["mothers_mean_age_first_birth"]["is_estimate"] = True

    return result


if __name__ == "__main__":
    test1 = {"text": "27 years (2019 est.)"}
    print(parse_mothers_age_at_first_birth(test1))
