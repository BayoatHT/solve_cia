import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_demographic_profile(demo_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse demographic profile text from CIA World Factbook format.

    This is a descriptive text field - we preserve it as-is.
    """
    if return_original:
        return demo_data

    result = {
        "demographic_profile": {
            "description": None
        },
        "demographic_profile_note": ""
    }

    if not demo_data or not isinstance(demo_data, dict):
        return result

    text = demo_data.get('text', '').strip()

    if text and text.upper() != 'NA':
        # Clean HTML tags if present
        text = re.sub(r'<[^>]+>', '', text).strip()
        result["demographic_profile"]["description"] = text

    return result


if __name__ == "__main__":
    test1 = {"text": "The demographic profile describes population characteristics."}
    print(parse_demographic_profile(test1))
