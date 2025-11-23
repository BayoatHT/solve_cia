import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_expenditures(military_expenditures_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Military Expenditures' data into a structured dictionary containing
    percentage value, unit, and date for each year, along with a note if provided.

    Parameters:
        military_expenditures_data (dict): The data section containing military expenditures.

    Returns:
        dict: A dictionary with structured information for military expenditures over the years.
    """
    result = {
        "military_note": clean_text(military_expenditures_data.get("note", ""))
    }

    # Updated regex pattern to extract the value, unit, and date, allowing optional text after the year
    expenditure_pattern = re.compile(
        r"([\d\.]+)% of GDP \((\d{4})\s*(?:est\.)?\)")

    # Loop through each key, looking for military expenditure entries by year
    for key, data in military_expenditures_data.items():
        # Skip the 'note' key as it’s already processed
        if key == "note":
            continue

        # Extract the year from the key (last 4 characters)
        year = key[-4:]
        expenditure_key = f"military_expenditure_{year}"

        # Initialize a dictionary structure for this expenditure
        result[expenditure_key] = {
            "value": 0,
            "unit": "%",
            "date": year
        }

        # Extract the text and parse value and date if present
        text = data.get("text", "")
        if not text:
            logging.warning(f"No data found in {key}")
            continue

        match = expenditure_pattern.match(text)
        if match:
            result[expenditure_key]["value"] = float(
                match.group(1))  # Value as a float
            result[expenditure_key]["date"] = match.group(
                2)  # Date from parentheses
        else:
            logging.warning(f"Data format unrecognized in {key}")

    return result


# Example usage
if __name__ == "__main__":
    military_expenditures_data = {
        "Military Expenditures 2024": {
            "text": "3.4% of GDP (2024 est.)"
        },
        "Military Expenditures 2023": {
            "text": "3.2% of GDP (2023)"
        },
        "Military Expenditures 2022": {
            "text": "3.3% of GDP (2022)"
        },
        "Military Expenditures 2021": {
            "text": "3.5% of GDP (2021)"
        },
        "Military Expenditures 2020": {
            "text": "3.6% of GDP (2020)"
        },
        "note": ""
    }
    parsed_data = parse_military_expenditures(military_expenditures_data)
    print(parsed_data)
