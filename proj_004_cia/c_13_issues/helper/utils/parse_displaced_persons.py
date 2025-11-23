import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_displaced_persons(displaced_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to displaced persons, including refugees, stateless persons, and internally displaced persons (IDPs).

    Parameters:
        displaced_data (dict): The dictionary containing displaced persons data.

    Returns:
        dict: A dictionary containing parsed information for refugees, stateless persons, and IDPs.
    """
    result = {
        "refugees_origin": [],
        "stateless_persons": {"value": "", "date": ""},
        "idp": {"year": 0, "causes": [], "number": 0}
    }

    # Handle 'refugees (country of origin)'
    refugees_data = displaced_data.get(
        "refugees (country of origin)", {}).get("text", "")
    if refugees_data:
        result["refugees_origin"] = parse_text_to_list(refugees_data)

    # Handle 'stateless persons'
    stateless_data = displaced_data.get(
        "stateless persons", {}).get("text", "")
    if stateless_data:
        match = re.match(r"(\d+)(?: \((\d{4})\))?", stateless_data)
        if match:
            result["stateless_persons"]["value"] = match.group(1)
            if match.group(2):
                result["stateless_persons"]["date"] = match.group(2)

    # Handle 'IDPs'
    idp_data = displaced_data.get("IDPs", {}).get("text", "")
    if idp_data:
        # Extract data from the IDP text
        main_pattern = re.compile(r'(\d+(?:,\d+)?(?:\.\d+)?)\s*(million)?')
        year_pattern = re.compile(r'\((\d{4})\)')
        causes_pattern = re.compile(r'\(([^)]+)\)')

        # Extract the main numeric value (e.g., "30,000" or "6.38 million")
        main_match = main_pattern.search(idp_data)
        if main_match:
            # Remove commas from the number string, if any
            number_str = main_match.group(1).replace(',', '')
            number = float(number_str)
            if main_match.group(2) == "million":
                number *= 1_000_000
            result["idp"]["number"] = number

        # Extract year (if available)
        year_match = year_pattern.search(idp_data)
        if year_match:
            result["idp"]["year"] = int(year_match.group(1))

        # Extract causes (non-numeric content in parentheses)
        causes_matches = causes_pattern.findall(idp_data)
        for cause in causes_matches:
            if not cause.isdigit() and not year_pattern.match(cause):
                # Split causes by semicolon and clean them
                causes = [cause_part.strip()
                          for cause_part in cause.split(';') if cause_part.strip()]
                result["idp"]["causes"].extend(causes)

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 3 >>> 'Refugees and internally displaced persons'
    # >>> ['idp', 'refugees_origin', 'stateless_persons']
    # ---------------------------------------------------------------------------------------------------------------------------
    displaced_data = {
        "refugees (country of origin)": {
            "text": "the US admitted 25,465 refugees during FY2022, including: 7,810 (Democratic Republic of the Congo), 4,556 (Syria), 2,156 (Burma), 1,669 (Sudan), 1,618 (Afghanistan), 1,610 (Ukraine)"
        },
        "stateless persons": {
            "text": "47 (2022)"
        },
        "IDPs": {
            "text": "6.38 million (fighting between government forces and rebels since mid-1990s; conflict in Kasai region since 2016) (2023)"
        }
    }
    parsed_data = parse_displaced_persons(displaced_data)
    print(parsed_data)
