import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_deployments(deployments_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to military deployments, including details and associated notes.

    Parameters:
        deployments_data (dict): The dictionary containing deployment data.

    Returns:
        dict: A dictionary containing parsed information for military deployments and notes.
    """
    result = {
        "mil_deploy": [],
        "mil_deploy_note": ""
    }

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

    return result


# Example usage
if __name__ == "__main__":
    # ['mil_deploy', 'mil_deploy_note']
    deployments_data = {
        "text": "the US has more than 200,000 air, ground, and naval personnel deployed overseas on a permanent or a long-term rotational (typically 3-9 months) basis; key areas of deployment include approximately 5,000 in Africa, approximately 100,000 in Europe, approximately 10-15,000 in Southwest Asia, and more than 80,000 in East Asia (2024)",
        "note": ""
    }
    parsed_data = parse_deployments(deployments_data)
    print(parsed_data)
