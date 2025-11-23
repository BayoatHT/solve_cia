import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_electricity(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "consumption" - 'electricity_consumption'
    # "exports" - 'electricity_exports'
    # "imports" - 'electricity_imports'
    # "installed generating capacity" - 'electricity_generating_capacity'
    # "note" - 'electricity_note'
    # "transmission/distribution losses" - 'electricity_transmission_distribution_losses'
    # --------------------------------------------------------------------------------------------------
    # ['electricity_consumption', 'electricity_exports', 'electricity_imports',
    # 'electricity_generating_capacity', 'electricity_note', 'electricity_transmission_distribution_losses']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "installed generating capacity": {
            "text": "1.201 billion kW (2022 est.)"
        },
        "consumption": {
            "text": "4.128 trillion kWh (2022 est.)"
        },
        "exports": {
            "text": "15.758 billion kWh (2022 est.)"
        },
        "imports": {
            "text": "56.97 billion kWh (2022 est.)"
        },
        "transmission/distribution losses": {
            "text": "204.989 billion kWh (2022 est.)"
        },
        "note": {
            "text": ""
        }
    }
    parsed_data = parse_electricity(pass_data)
    print(parsed_data)
