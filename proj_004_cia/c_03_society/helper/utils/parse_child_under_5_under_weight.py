import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_child_under_5_under_weight(child_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse children under 5 underweight data from CIA World Factbook format.

    Handles formats:
    1. Standard: "12.5% (2019)"
    2. Year range: "0.4% (2017/18)"
    3. With estimate: "10.2% (2020 est.)"
    4. NA values
    """
    if return_original:
        return child_data

    result = {
        "children_under_5_underweight": {
            "value": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "children_under_5_underweight_note": ""
    }

    if not child_data or not isinstance(child_data, dict):
        return result

    text = child_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    PATTERN = re.compile(r'([\d.]+)%\s*(?:\(([^)]+)\))?')
    match = PATTERN.search(text)
    if match:
        result["children_under_5_underweight"]["value"] = float(match.group(1))
        if match.group(2):
            year_info = match.group(2).strip()
            year_match = re.search(r'(\d{4}(?:/\d{2,4})?)', year_info)
            if year_match:
                result["children_under_5_underweight"]["timestamp"] = year_match.group(1)
            if 'est' in year_info.lower():
                result["children_under_5_underweight"]["is_estimate"] = True

    return result


if __name__ == "__main__":
    test1 = {"text": "0.4% (2017/18)"}
    print(parse_child_under_5_under_weight(test1))
