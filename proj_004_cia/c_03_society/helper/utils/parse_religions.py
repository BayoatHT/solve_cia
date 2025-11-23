import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_religions(religion_data: dict) -> dict:
    """

    """
    result = {}

    return result


# Example usage
if __name__ == "__main__":
    religion_data = {
        "text": "Protestant 46.5%, Roman Catholic 20.8%, Jewish 1.9%, Church of Jesus Christ 1.6%, other Christian 0.9%, Muslim 0.9%, Jehovah's Witness 0.8%, Buddhist 0.7%, Hindu 0.7%, other 1.8%, unaffiliated 22.8%, don't know/refused 0.6% (2014 est.)"
    }
    parsed_data = parse_religions(religion_data)
    print(parsed_data)
