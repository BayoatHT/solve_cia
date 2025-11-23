import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_env_current_issues(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'env_current_issues'
    # --------------------------------------------------------------------------------------------------
    # ['env_current_issues']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "air pollution; large emitter of carbon dioxide from the burning of fossil fuels; water pollution from runoff of pesticides and fertilizers; declining natural freshwater resources in much of the western part of the country require careful management; deforestation; mining; desertification; species conservation; invasive species (the Hawaiian Islands are particularly vulnerable)"
    }
    parsed_data = parse_env_current_issues(pass_data)
    print(parsed_data)
