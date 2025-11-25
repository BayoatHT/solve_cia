import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_nationality(nationality_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parse nationality data from CIA World Factbook format.

    Handles nested structure:
    {
        "noun": {"text": "Gibraltarian(s)"},
        "adjective": {"text": "Gibraltar"}
    }
    """
    if return_original:
        return nationality_data

    result = {
        "nationality": {
            "noun": None,
            "adjective": None
        },
        "nationality_note": ""
    }

    if not nationality_data or not isinstance(nationality_data, dict):
        return result

    if 'noun' in nationality_data:
        noun_data = nationality_data['noun']
        text = noun_data.get('text', '') if isinstance(noun_data, dict) else str(noun_data)
        if text and text.upper() != 'NA':
            result["nationality"]["noun"] = text.strip()

    if 'adjective' in nationality_data:
        adj_data = nationality_data['adjective']
        text = adj_data.get('text', '') if isinstance(adj_data, dict) else str(adj_data)
        if text and text.upper() != 'NA':
            result["nationality"]["adjective"] = text.strip()

    return result


if __name__ == "__main__":
    test1 = {
        "noun": {"text": "American(s)"},
        "adjective": {"text": "American"}
    }
    print(parse_nationality(test1))
