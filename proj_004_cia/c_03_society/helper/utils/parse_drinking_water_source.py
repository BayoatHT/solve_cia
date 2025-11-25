import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_drinking_water_source(water_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse drinking water source data from CIA World Factbook format.

    Handles nested structure with improved/unimproved and urban/rural/total.
    """
    if return_original:
        return water_data

    result = {
        "drinking_water_source": {
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
        "drinking_water_source_note": ""
    }

    if not water_data or not isinstance(water_data, dict):
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
        if field_name in water_data:
            field_data = water_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            pct, year, is_est = extract_percentage(text)
            result["drinking_water_source"][result_key] = pct
            if year and not result["drinking_water_source"]["timestamp"]:
                result["drinking_water_source"]["timestamp"] = year
                result["drinking_water_source"]["is_estimate"] = is_est

    return result


if __name__ == "__main__":
    test1 = {
        "improved: urban": {"text": "urban: 99.9% of population"},
        "improved: total": {"text": "total: 99.9% of population"},
        "unimproved: total": {"text": "total: 0.1% of population (2020 est.)"}
    }
    print(parse_drinking_water_source(test1))
