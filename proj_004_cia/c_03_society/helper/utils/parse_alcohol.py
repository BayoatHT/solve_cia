import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_alcohol(alcohol_data: dict, iso3Code: str = None) -> dict:
    """
    Parse alcohol consumption per capita from CIA World Factbook format.

    Handles nested structure:
    {
        "total": {"text": "8.93 liters of pure alcohol (2019 est.)"},
        "beer": {"text": "3.97 liters of pure alcohol (2019 est.)"},
        "wine": {"text": "1.67 liters of pure alcohol (2019 est.)"},
        "spirits": {"text": "3.29 liters of pure alcohol (2019 est.)"},
        "other alcohols": {"text": "0 liters of pure alcohol (2019 est.)"}
    }
    """
    result = {
        "alcohol_consumption": {
            "total": None,
            "beer": None,
            "wine": None,
            "spirits": None,
            "other": None,
            "unit": "liters of pure alcohol",
            "timestamp": None,
            "is_estimate": False
        },
        "alcohol_consumption_note": ""
    }

    if not alcohol_data or not isinstance(alcohol_data, dict):
        return result

    def extract_liters(text: str) -> tuple:
        if not text or text.upper() == 'NA':
            return None, None, False
        liters_match = re.search(r'([\d.]+)\s*liters?', text)
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        liters = float(liters_match.group(1)) if liters_match else None
        year = year_match.group(1) if year_match else None
        is_est = bool(year_match and year_match.group(2)) if year_match else False
        return liters, year, is_est

    field_map = {
        'total': 'total',
        'beer': 'beer',
        'wine': 'wine',
        'spirits': 'spirits',
        'other alcohols': 'other'
    }

    for field_name, result_key in field_map.items():
        if field_name in alcohol_data:
            field_data = alcohol_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            liters, year, is_est = extract_liters(text)
            result["alcohol_consumption"][result_key] = liters
            if year and not result["alcohol_consumption"]["timestamp"]:
                result["alcohol_consumption"]["timestamp"] = year
                result["alcohol_consumption"]["is_estimate"] = is_est

    return result


if __name__ == "__main__":
    test1 = {
        "total": {"text": "8.93 liters of pure alcohol (2019 est.)"},
        "beer": {"text": "3.97 liters of pure alcohol (2019 est.)"},
        "wine": {"text": "1.67 liters of pure alcohol (2019 est.)"},
        "spirits": {"text": "3.29 liters of pure alcohol (2019 est.)"},
        "other alcohols": {"text": "0 liters of pure alcohol (2019 est.)"}
    }
    print(parse_alcohol(test1))
