import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_net_migration_rate(migration_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    migration_data = {
        "text": "3 migrant(s)/1,000 population (2024 est.)"
    }
    parsed_data = parse_net_migration_rate(migration_data)
    print(parsed_data)
