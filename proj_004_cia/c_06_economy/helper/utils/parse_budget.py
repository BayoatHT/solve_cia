import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_budget(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses budget data for expenditures and revenues, capturing value, unit, and date.

    Parameters:
        pass_data (dict): The dictionary containing budget data.

    Returns:
        dict: A dictionary with keys `budget_expenditures` and `budget_revenues` containing
              dictionaries with `value`, `unit`, and `date`.
    """
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

        # Skip NA values
        if item.upper().strip() == 'NA':
            result[result_key]["value"] = None
            result[result_key]["note"] = "NA"
            continue

        # Try multiple patterns
        # Pattern 1: $X.XXX trillion/billion/million (YYYY est.)
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)\s+\((\d{4})\s+est\.\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            year = match.group(3)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            result[result_key]["date"] = year
            continue

        # Pattern 2: $X.XXX trillion/billion/million (YYYY) - without "est."
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)\s+\((\d{4})\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            year = match.group(3)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            result[result_key]["date"] = year
            continue

        # Pattern 3: $X.XXX million (FYXX/XX est.) - fiscal year format
        match = re.match(r"\$([\d,.]+)\s+(trillion|billion|million)\s+\(FY\d{2}/\d{2}(?:\s+est\.)?\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            unit = match.group(2)
            multipliers = {"trillion": 1e12, "billion": 1e9, "million": 1e6}
            result[result_key]["value"] = float(value_str) * multipliers.get(unit, 1)
            result[result_key]["date"] = ""  # Don't extract FY format
            continue

        # Pattern 4: $X,XXX,XXX (YYYY est.) - raw numbers with commas
        match = re.match(r"\$([\d,]+)\s+\((\d{4})\s+est\.\)", item)
        if match:
            value_str = match.group(1).replace(",", "")
            year = match.group(2)
            result[result_key]["value"] = float(value_str)
            result[result_key]["date"] = year
            continue

        # If we couldn't parse, set to None and log warning
        if item:
            result[result_key]["value"] = None
            result[result_key]["note"] = f"Unparsed: {item}"
            logging.debug(f"Could not parse budget {key}: {item}")

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
