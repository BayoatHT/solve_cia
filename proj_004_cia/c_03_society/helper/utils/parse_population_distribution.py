import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_population_distribution(pop_distro_data: dict, iso3Code: str = None) -> dict:
    """
    Parse population distribution text from CIA World Factbook format.

    This is a descriptive text field - we preserve it as-is.
    """
    result = {
        "population_distribution": {
            "description": None
        },
        "population_distribution_note": ""
    }

    if not pop_distro_data or not isinstance(pop_distro_data, dict):
        return result

    text = pop_distro_data.get('text', '').strip()

    if text and text.upper() != 'NA':
        # Clean HTML tags if present
        text = re.sub(r'<[^>]+>', '', text).strip()
        result["population_distribution"]["description"] = text

    return result


if __name__ == "__main__":
    test1 = {
        "text": "large urban clusters are spread throughout the eastern half of the US"
    }
    print(parse_population_distribution(test1))
