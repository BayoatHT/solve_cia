import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_env_current_issues(issues_data: dict, iso3Code: str = None) -> dict:
    """
    Parse environment current issues data from CIA World Factbook format.

    Args:
        issues_data: Dictionary with environment issues information
        iso3Code: Optional ISO3 country code for logging

    Returns:
        Dictionary with structured issues data
    """
    result = {
        "env_current_issues": {
            "description": None,
            "issues_list": []
        },
        "env_current_issues_note": ""
    }

    if not issues_data or not isinstance(issues_data, dict):
        return result

    text = issues_data.get('text', '')
    if text and text.upper() != 'NA':
        cleaned = clean_text(text)
        result['env_current_issues']['description'] = cleaned

        # Try to parse issues into a list (separated by semicolons or commas)
        if cleaned:
            # Split by semicolons first
            issues = [i.strip() for i in cleaned.split(';') if i.strip()]
            if len(issues) == 1:
                # Try commas if no semicolons
                issues = [i.strip() for i in cleaned.split(',') if i.strip()]
            result['env_current_issues']['issues_list'] = issues

    return result


if __name__ == "__main__":
    test_data = {
        "text": "air pollution; water pollution from runoff; deforestation"
    }
    print(parse_env_current_issues(test_data))
