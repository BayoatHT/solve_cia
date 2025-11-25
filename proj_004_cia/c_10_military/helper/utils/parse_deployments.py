import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_deployments(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse military deployments data from CIA Military and Security section.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary containing parsed information for military deployments and notes.
    """
    result = {
        "mil_deploy": [],
        "mil_deploy_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    deployments_data = military_section.get('Military deployments', {})

    if return_original:
        return deployments_data


    if not deployments_data or not isinstance(deployments_data, dict):
        return result

    try:
        # Handle 'text'
        deploy_text = deployments_data.get("text", "")
        if deploy_text:
            result["mil_deploy"] = parse_text_to_list(deploy_text)

        # Handle 'note'
        deploy_note = deployments_data.get("note", "")
        if deploy_note:
            clean_note = re.sub(r'<strong>note:</strong>\s*',
                                '', deploy_note, flags=re.IGNORECASE)
            result["mil_deploy_note"] = clean_text(clean_note)

    except Exception as e:
        logger.error(f"Error parsing deployments for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_deployments")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'FRA', 'GBR', 'DEU']:
        print(f"\n{iso3}:")
        try:
            result = parse_deployments(iso3)
            if result.get('mil_deploy'):
                deploy = result['mil_deploy']
                print(f"  Deployment entries: {len(deploy)}")
                if deploy:
                    print(f"    First: {str(deploy[0])[:60]}...")
            else:
                print("  No deployment data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
