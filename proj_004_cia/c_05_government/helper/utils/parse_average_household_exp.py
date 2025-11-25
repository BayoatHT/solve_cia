import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_average_household_exp(pass_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses average household expenditures data for food and alcohol/tobacco.

    Parameters:
        pass_data (dict): The dictionary containing household expenditure data.

    Returns:
        dict: A dictionary with keys `avg_house_expend_food` and `avg_house_expend_alcohol_tobacco` containing
              dictionaries with `value`, `unit`, and `date`.
    """
    if return_original:
        return pass_data

    result = {}

    # Define mapping for keys
    expenditure_keys = {
        "on food": "avg_house_expend_food",
        "on alcohol and tobacco": "avg_house_expend_alcohol_tobacco"
    }

    for key, result_key in expenditure_keys.items():
        item = pass_data.get(key, {}).get("text", "")

        # Define default values for result
        result[result_key] = {"value": 0, "unit": "%", "date": ""}

        # Match the pattern for value, unit, and date
        match = re.match(
            r"([\d.]+)% of household expenditures \((\d{4}) est\.\)", item)

        if match:
            result[result_key]["value"] = float(match.group(1))
            result[result_key]["date"] = match.group(2)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 3 >>> 'Average household expenditures'
    # --------------------------------------------------------------------------------------------------
    # "on alcohol and tobacco" - 'avg_house_expend_alcohol_tobacco'
    # "on food" - 'avg_house_expend_food'
    # --------------------------------------------------------------------------------------------------
    # ['avg_house_expend_alcohol_tobacco', 'avg_house_expend_food']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "on food": {
            "text": "6.7% of household expenditures (2021 est.)"
        },
        "on alcohol and tobacco": {
            "text": "1.9% of household expenditures (2021 est.)"
        }
    }
    parsed_data = parse_average_household_exp(pass_data)
    print(parsed_data)
