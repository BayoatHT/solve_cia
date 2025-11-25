import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_budget_surplus_deficit(pass_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the budget surplus/deficit data and applies clean_text.

    Parameters:
        pass_data (dict): The dictionary containing budget surplus/deficit data.

    Returns:
        dict: A dictionary with a single cleaned key-value pair for budget_surplus_deficit.
    """
    if return_original:
        return pass_data

    result = {}

    # Clean the text value and store it in the result dictionary
    result['budget_surplus_deficit'] = clean_text(pass_data.get("text", ""))

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # text - 'budget_surplus_deficit'
    # --------------------------------------------------------------------------------------------------
    # ['budget_surplus_deficit']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "text": "NA"
    }
    parsed_data = parse_budget_surplus_deficit(pass_data)
    print(parsed_data)
