import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_population_growth(pop_growth_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    pop_growth_data = {
        "text": "0.67% (2024 est.)"
    }
    parsed_data = parse_population_growth(pop_growth_data)
    print(parsed_data)
