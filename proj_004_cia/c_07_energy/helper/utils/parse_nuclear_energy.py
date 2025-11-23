import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_nuclear_energy(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Net capacity of operational nuclear reactors" - 'nuclear_operational_reactors_capacity'
    # "Number of nuclear reactors permanently shut down" - 'nuclear_reactors_shut_down'
    # "Number of nuclear reactors under construction" - 'nuclear_reactors_under_construction'
    # "Number of operational nuclear reactors" - 'nuclear_operational_reactors'
    # "Percent of total electricity production" - 'nuclear_percent_total_electricity'
    # --------------------------------------------------------------------------------------------------
    # ['nuclear_operational_reactors_capacity', 'nuclear_reactors_shut_down', 'nuclear_reactors_under_construction',
    # 'nuclear_operational_reactors', 'nuclear_percent_total_electricity']
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Number of operational nuclear reactors": {
            "text": "94 (2023)"
        },
        "Net capacity of operational nuclear reactors": {
            "text": "96.95GW (2023 est.)"
        },
        "Percent of total electricity production": {
            "text": "18.5% (2023 est.)"
        },
        "Number of nuclear reactors permanently shut down": {
            "text": "41 (2023)"
        }
    }
    parsed_data = parse_nuclear_energy(pass_data)
    print(parsed_data)
