import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_child_marriage(child_marriage_data: dict, iso3Code: str = None) -> dict:
    """
    Parse child marriage data from CIA World Factbook format.

    Handles nested structure:
    {
        "women married by age 15": {"text": "0%"},
        "women married by age 18": {"text": "5.3%"},
        "men married by age 18": {"text": "0.4% (2016 est.)"}
    }
    """
    result = {
        "child_marriage": {
            "women_by_15": None,
            "women_by_18": None,
            "men_by_18": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "child_marriage_note": ""
    }

    if not child_marriage_data or not isinstance(child_marriage_data, dict):
        return result

    def extract_percentage(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False
        pct_match = re.search(r'([\d.]+)%', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        pct = float(pct_match.group(1)) if pct_match else None
        year = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False
        return pct, year, is_est

    field_map = {
        'women married by age 15': 'women_by_15',
        'women married by age 18': 'women_by_18',
        'men married by age 18': 'men_by_18'
    }

    for field_name, result_key in field_map.items():
        if field_name in child_marriage_data:
            field_data = child_marriage_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            pct, year, is_est = extract_percentage(text)
            result["child_marriage"][result_key] = pct
            if year and not result["child_marriage"]["timestamp"]:
                result["child_marriage"]["timestamp"] = year
                result["child_marriage"]["is_estimate"] = is_est

    return result


if __name__ == "__main__":
    test1 = {
        "women married by age 15": {"text": "0%"},
        "women married by age 18": {"text": "5.3%"},
        "men married by age 18": {"text": "0.4% (2016 est.)"}
    }
    print(parse_child_marriage(test1))
