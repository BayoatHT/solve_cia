import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_revenue_from_forest(forest_data: dict, iso3Code: str = None) -> dict:
    """Parse revenue from forest resources data."""
    result = {
        "revenue_forest": {
            "value": None,
            "unit": "% of GDP",
            "timestamp": None,
            "is_estimate": False
        },
        "revenue_forest_note": ""
    }

    if not forest_data or not isinstance(forest_data, dict):
        return result

    text = forest_data.get('text', '')
    if text and text.upper() != 'NA':
        # Extract percentage
        pct_match = re.search(r'([\d.]+)%', text)
        if pct_match:
            result['revenue_forest']['value'] = float(pct_match.group(1))

        # Extract year
        year_match = re.search(r'\((\d{4})\s*(est\.?)?\)', text)
        if year_match:
            result['revenue_forest']['timestamp'] = year_match.group(1)
            result['revenue_forest']['is_estimate'] = 'est' in text.lower()

    return result


if __name__ == "__main__":
    test_data = {"text": "0.04% of GDP (2018 est.)"}
    print(parse_revenue_from_forest(test_data))
