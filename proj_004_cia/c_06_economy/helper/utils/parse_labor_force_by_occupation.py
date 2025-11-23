import re
import logging
from typing import Dict, Any
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_labor_force_by_occupation(pass_data: Dict[str, Any], iso3Code: str = None) -> Dict[str, Any]:
    """
    Parses labor force data by occupation, extracting percentage and year if available.

    Parameters:
        pass_data (dict): The dictionary containing labor force occupation data.

    Returns:
        dict: A dictionary with parsed data for labor force by occupation and year.
    """
    result = {}

    for key, value in pass_data.items():
        # Define the base key name based on the occupation
        base_key = f"labor_force_{key.replace(' ', '_').lower()}"

        # Extract the text value
        text = value.get("text", "")

        # Extract percentage and year if available
        match = re.match(r"([\d.]+)%(?: \((\d{4}) est\.\))?", text)
        if match:
            percentage = float(match.group(1))
            year = int(match.group(2)) if match.group(2) else ""
            result[base_key] = {
                "percentage": percentage,
                "year": year
            }
        else:
            logging.warning(
                f"Unexpected format in 'text' data for {key}: {text}")

    return result


# Example usage
if __name__ == "__main__":
    # NOTE: 31 >>> 'Labor force - by occupation'
    # --------------------------------------------------------------------------------------------------
    # "agriculture" - 'labor_force_agriculture'
    # "industry" - 'labor_force_industry'
    # "industry and services" - 'labor_force_industry_services'
    # --------------------------------------------------------------------------------------------------
    # ['labor_force_agriculture', 'labor_force_industry', 'labor_force_industry_services']
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    # --------------------------------------------------------------------------------------------------
    pass_data = {
        "agriculture": {
            "text": "50%"
        },
        "industry": {
            "text": "50%"
        },
        "industry and services": {
            "text": "50% (2005 est.)"
        }
    }
    parsed_data = parse_labor_force_by_occupation(pass_data)
    print(parsed_data)
