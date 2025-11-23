import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_remittances(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses remittance data, extracting the percentage of GDP and year from each entry.

    Parameters:
        pass_data (dict): The dictionary containing remittance data.

    Returns:
        dict: A dictionary with parsed data for remittances by year and additional notes.
    """
    result = {}

    for key, value in pass_data.items():
        if key == "note":
            # Process 'note' field
            result["remittances_note"] = clean_text(value)
        else:
            # Extract the year from the key
            year_match = re.search(r'\d{4}', key)
            if not year_match:
                logging.warning(f"No year found in key: {key}")
                continue

            year = year_match.group(0)

            # Process 'text' field for percentage and year
            text = value.get("text", "")
            match = re.match(r"([\d.]+)% of GDP \((\d{4})", text)
            if match:
                percentage = float(match.group(1))
                result[f"remittances_{year}"] = {
                    "percentage_of_gdp": percentage,
                    "year": int(year)
                }
            else:
                logging.warning(f"Unexpected format in 'text' data: {text}")

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 37 >>> 'Remittances'
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Remittances 2023": {
            "text": "0.31% of GDP (2023 est.)"
        },
        "Remittances 2022": {
            "text": "0.34% of GDP (2022 est.)"
        },
        "Remittances 2021": {
            "text": "0.32% of GDP (2021 est.)"
        },
        "note": "<b>note:</b> personal transfers and compensation between resident and non-resident individuals/households/entities"
    }
    parsed_data = parse_remittances(pass_data)
    print(parsed_data)
