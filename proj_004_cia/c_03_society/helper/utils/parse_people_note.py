import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_people_note(people_data: dict, iso3Code: str = None) -> dict:
    """
    Parse people/society note from CIA World Factbook format.

    This is a descriptive text field - we preserve it as-is.
    """
    result = {
        "people_note": {
            "text": None
        }
    }

    if not people_data or not isinstance(people_data, dict):
        return result

    text = people_data.get('text', '').strip()

    if text and text.upper() != 'NA':
        # Clean HTML tags
        text = re.sub(r'<[^>]+>', '', text).strip()
        result["people_note"]["text"] = text

    return result


if __name__ == "__main__":
    test1 = {"text": "This is a note about the population."}
    print(parse_people_note(test1))
