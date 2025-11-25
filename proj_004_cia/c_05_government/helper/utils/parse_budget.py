import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_budget(pass_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses budget data for expenditures and revenues, capturing value, unit, and date.

    Parameters:
        pass_data (dict): The dictionary containing budget data.

    Returns:
        dict: A dictionary with keys `budget_expenditures` and `budget_revenues` containing
              dictionaries with `value`, `unit`, and `date`.
    """
    if return_original:
        return pass_data

    result = {}

    # Define mapping for keys
    budget_keys = {
        "revenues": "budget_revenues",
        "expenditures": "budget_expenditures"
    }

    for key, result_key in budget_keys.items():
        item = pass_data.get(key, {}).get("text", "")

        # Define default values for result
        result[result_key] = {"value": 0, "unit": "$", "date": ""}

        # Match the pattern for value, unit, and date
        match = re.match(r"\$([\d,.]+) trillion \((\d{4}) est\.\)", item)

        if match:
            # Remove commas from value and convert to float, multiplying by a trillion (10^12)
            result[result_key]["value"] = float(
                match.group(1).replace(",", "")) * 1e12
            result[result_key]["date"] = match.group(2)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 4 >>> 'Budget'
    # --------------------------------------------------------------------------------------------------
    # "expenditures" - 'budget_expenditures'
    # "note" - 'budget_note'
    # "revenues" - 'budget_revenues'
    # --------------------------------------------------------------------------------------------------
    # ['budget_expenditures', 'budget_note', 'budget_revenues']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "revenues": {
            "text": "$6.429 trillion (2019 est.)"
        },
        "expenditures": {
            "text": "$7.647 trillion (2019 est.)"
        }
    }
    parsed_data = parse_budget(pass_data)
    print(parsed_data)
