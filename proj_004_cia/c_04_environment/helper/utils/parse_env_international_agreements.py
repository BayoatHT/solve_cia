import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_env_international_agreements(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "party to"- 'env_international_agreements_party_to'
    # "signed, but not ratified" - 'env_international_agreements_signed'
    # --------------------------------------------------------------------------------------------------
    # ['env_international_agreements_party_to', 'env_international_agreements_signed']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {

    }
    parsed_data = parse_env_international_agreements(pass_data)
    print(parsed_data)
