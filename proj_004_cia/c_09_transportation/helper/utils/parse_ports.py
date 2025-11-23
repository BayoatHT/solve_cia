import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ports(ports_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # "key ports" - key_ports
    # "large" - large_ports
    # "medium" - medium_ports
    # "ports with oil terminals" - 'ports_with_oil_terminals'
    # "size unknown" - ports_size_unknown
    # "small" - small_ports
    # "total ports" - total_ports
    # "very small" - very_small_ports
    # --------------------------------------------------------------------------------------------------
    # ['key_ports', 'large_ports', 'medium_ports', 'ports_with_oil_terminals', 'ports_size_unknown',
    # 'small_ports', 'total_ports', 'very_small_ports']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    ports_data = {
        "total ports": {
            "text": "666 (2024)"
        },
        "large": {
            "text": "21"
        },
        "medium": {
            "text": "38"
        },
        "small": {
            "text": "132"
        },
        "very small": {
            "text": "475"
        },
        "ports with oil terminals": {
            "text": "204"
        },
        "key ports": {
            "text": "Baltimore, Boston, Brooklyn, Buffalo, Chester, Cleveland, Detroit, Galveston, Houston, Los Angeles, Louisiana Offshore Oil Port (LOOP), Mobile, New Orleans, New York City, Norfolk, Oakland, Philadelphia, Portland, San Francisco, Seattle, Tri-City Port"
        }
    }
    parsed_data = parse_ports(ports_data)
    print(parsed_data)
