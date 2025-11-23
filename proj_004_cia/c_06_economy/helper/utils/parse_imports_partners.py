import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_imports_partners(pass_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 26 >>> 'Imports - partners'
    # --------------------------------------------------------------------------------------------------
    # "note" - 'imports_partners_note'
    # "text" - 'imports_partners'
    # --------------------------------------------------------------------------------------------------
    # ['imports_partners', 'imports_partners_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "China 18%, Canada 14%, Mexico 14%, Germany 5%, Japan 4% (2022)",
        "note": "<b>note:</b> top five import partners based on percentage share of imports"
    }
    parsed_data = parse_imports_partners(pass_data)
    print(parsed_data)
