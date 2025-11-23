import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_geoparks(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "global geoparks and regional networks" - 'env_global_geoparks_reg_networks'
    # "total global geoparks and regional networks" - "env_total_geoparks_reg_networks"
    # --------------------------------------------------------------------------------------------------
    # ['env_global_geoparks_reg_networks', 'env_total_geoparks_reg_networks']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {

    }
    parsed_data = parse_geoparks(pass_data)
    print(parsed_data)
