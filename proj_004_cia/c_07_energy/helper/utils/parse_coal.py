import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_coal(coal_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "consumption" - 'coal_consumption'
    # "exports" - 'coal_exports'
    # "imports" - 'coal_imports'
    # "note" - 'coal_note'
    # "production"- 'coal_production'
    # "proven reserves" - 'coal_proven_reserves'
    # --------------------------------------------------------------------------------------------------
    # ['coal_consumption', 'coal_exports', 'coal_imports', 'coal_note',
    # 'coal_production', 'coal_proven_reserves']
    # --------------------------------------------------------------------------------------------------
    coal_data = {
        "production": {
            "text": "548.849 million metric tons (2022 est.)"
        },
        "consumption": {
            "text": "476.044 million metric tons (2022 est.)"
        },
        "exports": {
            "text": "80.081 million metric tons (2022 est.)"
        },
        "imports": {
            "text": "5.788 million metric tons (2022 est.)"
        },
        "proven reserves": {
            "text": "248.941 billion metric tons (2022 est.)"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_coal(coal_data)
    print(parsed_data)
