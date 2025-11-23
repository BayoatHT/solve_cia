import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_broadband_fixed(broadband_fixed_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    # "note" - 'broadband_note'
    # "subscriptions per 100 inhabitants" - 'broadband_subs_per_100'
    # "total" - 'broadband_total'
    # --------------------------------------------------------------------------------------------------
    # ['broadband_note', 'broadband_subs_per_100', 'broadband_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    broadband_fixed_data = {
        "total": {
            "text": "121.176 million (2020 est.)"
        },
        "subscriptions per 100 inhabitants": {
            "text": "37 (2020 est.)"
        }
    }
    parsed_data = parse_broadband_fixed(broadband_fixed_data)
    print(parsed_data)
