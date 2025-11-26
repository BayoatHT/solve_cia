import re
import logging
from typing import Dict, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_env_current_issues(issues_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse environment current issues from CIA Environment section for a given country.

    Args:
        issues_data: The 'Environment - current issues' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured environmental issues data
    """
    result = {
        "env_current_issues": {
            "description": None,
            "issues_list": []
        },
        "env_current_issues_note": ""
    }

    if return_original:
        return issues_data

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
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_env_current_issues")
    print("="*60)
    for iso3 in ['USA', 'CHN', 'IND', 'BRA', 'RUS', 'DEU']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            issues_data = raw_data.get('Environment', {}).get('Environment - current issues', {})
            result = parse_env_current_issues(issues_data, iso3)
            if result and result['env_current_issues']['issues_list']:
                issues = result['env_current_issues']['issues_list']
                print(f"  Found {len(issues)} issues:")
                for issue in issues[:3]:
                    print(f"    - {issue[:50]}...")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
