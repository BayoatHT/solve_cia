import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_sanitation_access(sanitation_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse sanitation facility access data from CIA World Factbook format.

    Handles nested structure with improved/unimproved and urban/rural/total.
    """
    if return_original:
        return sanitation_data

    result = {
        "sanitation_access": {
            "improved_urban": None,
            "improved_rural": None,
            "improved_total": None,
            "unimproved_urban": None,
            "unimproved_rural": None,
            "unimproved_total": None,
            "unit": "% of population",
            "timestamp": None,
            "is_estimate": False
        },
        "sanitation_access_note": ""
    }

    if not sanitation_data or not isinstance(sanitation_data, dict):
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
        'improved: urban': 'improved_urban',
        'improved: rural': 'improved_rural',
        'improved: total': 'improved_total',
        'unimproved: urban': 'unimproved_urban',
        'unimproved: rural': 'unimproved_rural',
        'unimproved: total': 'unimproved_total'
    }

    for field_name, result_key in field_map.items():
        if field_name in sanitation_data:
            field_data = sanitation_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            pct, year, is_est = extract_percentage(text)
            result["sanitation_access"][result_key] = pct
            if year and not result["sanitation_access"]["timestamp"]:
                result["sanitation_access"]["timestamp"] = year
                result["sanitation_access"]["is_estimate"] = is_est

    return result


if __name__ == "__main__":
    test1 = {
        "improved: urban": {"text": "urban: 99.8% of population"},
        "improved: total": {"text": "total: 99.7% of population"},
        "unimproved: total": {"text": "total: 0.3% of population (2020 est.)"}
    }
    print(parse_sanitation_access(test1))
