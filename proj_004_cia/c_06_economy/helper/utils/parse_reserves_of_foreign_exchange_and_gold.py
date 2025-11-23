import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_reserves_of_foreign_exchange_and_gold(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses reserves of foreign exchange and gold data, extracting the value, unit, and year.

    Parameters:
        pass_data (dict): The dictionary containing reserves data.

    Returns:
        dict: A dictionary with parsed data for reserves of foreign exchange and gold.
    """
    result = {}

    for key, value in pass_data.items():
        if key == "note":
            # Process 'note' field
            result["reserves_note"] = clean_text(value)
        else:
            # Extract the year from the key
            year_match = re.search(r'\d{4}', key)
            if not year_match:
                logging.warning(f"No year found in key: {key}")
                continue

            year = year_match.group(0)

            # Process 'text' field for value and unit
            text = value.get("text", "")
            match = re.match(r"\$(\d[\d,.]*)\s*(\w+)\s*\((\d{4})", text)
            if match:
                value_num = float(match.group(1).replace(",", ""))
                unit = match.group(2)
                result[f"reserves_{year}"] = {
                    "value": value_num,
                    "unit": unit,
                    "year": int(year)
                }
            else:
                logging.warning(f"Unexpected format in 'text' data: {text}")

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 38 >>> 'Reserves of foreign exchange and gold'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Reserves of foreign exchange and gold 2023": {
            "text": "$4.756 billion (2023 est.)"
        },
        "Reserves of foreign exchange and gold 2022": {
            "text": "$4.279 billion (2022 est.)"
        },
        "Reserves of foreign exchange and gold 2021": {
            "text": "$4.802 billion (2021 est.)"
        },
        "note": "<b>note:</b> holdings of gold (year-end prices)/foreign exchange/special drawing rights in current dollars"
    }
    parsed_data = parse_reserves_of_foreign_exchange_and_gold(pass_data)
    print(parsed_data)
