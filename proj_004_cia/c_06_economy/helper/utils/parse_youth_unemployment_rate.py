import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_youth_unemployment_rate(pass_data: dict, iso3Code: str = None) -> dict:
    """
    Parses youth unemployment data for total, male, and female categories, extracting
    the unemployment percentage and year, and processing notes if available.

    Parameters:
        pass_data (dict): The dictionary containing youth unemployment data.

    Returns:
        dict: A dictionary with parsed youth unemployment data.
    """
    result = {}

    # Define keys to process
    categories = {
        "total": "youth_unemployment_total",
        "male": "youth_unemployment_male",
        "female": "youth_unemployment_female"
    }

    # Parse each category
    for key, result_key in categories.items():
        if key in pass_data:
            text = pass_data[key].get("text", "")
            # Handle formats like "45.4% (2023 est.)" or just "17.5%"
            match = re.match(r"([\d.]+)%(?:\s*\((\d{4}))?", text)
            if match:
                result[result_key] = {
                    "value": float(match.group(1)),
                    "year": int(match.group(2)) if match.group(2) else None
                }
            elif text and text.upper() != 'NA':
                # Only warn if there's actual text that couldn't be parsed (not NA)
                logging.warning(f"Unexpected format in '{key}' data: {text}")

    # Handle 'note' if present
    if "note" in pass_data:
        result["youth_unemployment_note"] = clean_text(pass_data["note"])

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # "female" - 'youth_unemployment_female'
    # "male" - 'youth_unemployment_male'
    # "note" - 'youth_unemployment_note'
    # "total" - 'youth_unemployment_total'
    # --------------------------------------------------------------------------------------------------
    # ['youth_unemployment_female', 'youth_unemployment_male', 'youth_unemployment_note', 'youth_unemployment_total']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "total": {
            "text": "45.4% (2023 est.)"
        },
        "male": {
            "text": "40.5% (2023 est.)"
        },
        "female": {
            "text": "51.5% (2023 est.)"
        },
        "note": "<b>note:</b> % of labor force ages 15-24 seeking employment"
    }
    parsed_data = parse_youth_unemployment_rate(pass_data)
    print(parsed_data)
