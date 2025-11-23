import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_unemployment_rate(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses the unemployment rate data, extracting values and years for each entry and handling notes.

    Parameters:
        pass_data (dict): The dictionary containing unemployment rate data.

    Returns:
        dict: A dictionary with parsed unemployment rate data by year and any associated notes.
    """
    result = {}

    # Process each key in pass_data
    for key, data in pass_data.items():
        # Match keys that contain a year
        year_match = re.search(r"(\d{4})", key)
        if year_match:
            year = year_match.group(1)
            text = data.get("text", "")
            # Extract value and year from text
            match = re.match(r"([\d.]+)%\s*\((\d{4})", text)
            if match:
                result[f"unemploy_rate_{year}"] = {
                    "value": float(match.group(1)),
                    "year": int(match.group(2))
                }
            else:
                logging.warning(f"Unexpected format in '{key}' data: {text}")
        elif key == "note":
            data = data.replace("note:", "")
            # Handle 'note' key
            result["unemploy_rate_note"] = clean_text(data)

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "Unemployment rate 2014" - 'unemploy_rate_2014'
    # "Unemployment rate 2015" - 'unemploy_rate_2015'
    # "Unemployment rate 2016" - 'unemploy_rate_2016'
    # "Unemployment rate 2017" - 'unemploy_rate_2017'
    # "Unemployment rate 2018" - 'unemploy_rate_2018'
    # "Unemployment rate 2019" - 'unemploy_rate_2019'
    # "Unemployment rate 2020" - 'unemploy_rate_2020'
    # "Unemployment rate 2021" - 'unemploy_rate_2021'
    # "Unemployment rate 2022" - 'unemploy_rate_2022'
    # "Unemployment rate 2023" - 'unemploy_rate_2023'
    # "note" - 'unemploy_rate_note'
    # --------------------------------------------------------------------------------------------------
    # ['unemploy_rate_2014', 'unemploy_rate_2015', 'unemploy_rate_2016', 'unemploy_rate_2017',
    # 'unemploy_rate_2018', 'unemploy_rate_2019', 'unemploy_rate_2020', 'unemploy_rate_2021',
    # 'unemploy_rate_2022', 'unemploy_rate_2023', 'unemploy_rate_note']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "Unemployment rate 2023": {
            "text": "23.38% (2023 est.)"
        },
        "Unemployment rate 2022": {
            "text": "23.62% (2022 est.)"
        },
        "Unemployment rate 2021": {
            "text": "23.11% (2021 est.)"
        },
        "note": "<b>note:</b> % of labor force seeking employment"
    }
    parsed_data = parse_unemployment_rate(pass_data)
    print(parsed_data)
