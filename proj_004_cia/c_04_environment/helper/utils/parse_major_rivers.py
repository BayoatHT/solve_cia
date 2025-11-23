import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_major_rivers(pass_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'env_major_rivers'
    # --------------------------------------------------------------------------------------------------
    # ['env_major_rivers']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "<p>Missouri - 3,768 km; Mississippi - 3,544 km; Yukon river mouth (shared with Canada [s]) - 3,190 km; Saint Lawrence (shared with Canada) - 3,058 km; Rio Grande river source ( mouth shared with Mexico) - 3,057 km; Colorado river source (shared with Mexico [m]) - 2,333 km; Arkansas - 2,348 km; Columbia river mouth (shared with Canada [s]) - 2,250 km; Red - 2,188 km; Ohio - 2,102 km; Snake - 1,670 km<br><strong>note</strong> – [s] after country name indicates river source; [m] after country name indicates river mouth</p>"
    }
    parsed_data = parse_major_rivers(pass_data)
    print(parsed_data)
