import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_tobacco_use(tobacco_data: dict, iso3Code: str = None) -> dict:
    """
    Parse tobacco use data from CIA World Factbook format.

    Handles nested structure:
    {
        "total": {"text": "25.5% (2020 est.)"},
        "male": {"text": "28.1% (2020 est.)"},
        "female": {"text": "22.9% (2020 est.)"}
    }
    """
    result = {
        "tobacco_use": {
            "total": None,
            "male": None,
            "female": None,
            "unit": "%",
            "timestamp": None,
            "is_estimate": False
        },
        "tobacco_use_note": ""
    }

    if not tobacco_data or not isinstance(tobacco_data, dict):
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

    for field_name in ['total', 'male', 'female']:
        if field_name in tobacco_data:
            field_data = tobacco_data[field_name]
            text = field_data.get('text', '') if isinstance(field_data, dict) else str(field_data)
            pct, year, is_est = extract_percentage(text)
            result["tobacco_use"][field_name] = pct
            if year and not result["tobacco_use"]["timestamp"]:
                result["tobacco_use"]["timestamp"] = year
                result["tobacco_use"]["is_estimate"] = is_est

    return result


if __name__ == "__main__":
    test1 = {
        "total": {"text": "23% (2020 est.)"},
        "male": {"text": "28.4% (2020 est.)"},
        "female": {"text": "17.5% (2020 est.)"}
    }
    print(parse_tobacco_use(test1))
