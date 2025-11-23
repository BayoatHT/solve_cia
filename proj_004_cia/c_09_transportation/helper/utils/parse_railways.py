import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_railways(railways_data: dict, iso3Code: str = None) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # "broad gauge" - 'railways_broad'
    # "dual gauge" - 'railways_dual'
    # "narrow gauge" - 'railways_narrow'
    # "note" - 'railways_note'
    # "standard gauge" - 'railways_standard'
    # "total" - 'railways_total'
    # --------------------------------------------------------------------------------------------------
    # ['railways_broad', 'railways_dual', 'railways_narrow', 'railways_note', 'railways_standard', 'railways_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    railways_data = {
        "total": {
            "text": "293,564.2 km (2014)"
        },
        "broad gauge": {
            "text": "2,707 km (2022) 1.000 m guage"
        },
        "standard gauge": {
            "text": "293,564.2 km (2014) 1.435-m gauge"
        },
        "narrow gauge": {
            "text": "438 km (2014) 1.000-m gauge"
        },
        "dual gauge": {
            "text": "8 km (2014) 1.435-1.000-m gauge"
        },
        "note": "22,207 km 1.067-mm gauge (15,430 km electrified)<br>48 km 0.762-m gauge (48 km electrified)"
    }
    parsed_data = parse_railways(railways_data)
    print(parsed_data)
