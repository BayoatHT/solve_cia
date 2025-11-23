import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_population(population_data: dict) -> dict:
    """
    Parses the 'Population' data for a country.

    Parameters:
        population_data (dict): The 'Population' section from the data.

    Returns:
        dict: A dictionary containing parsed details of population.
    """
    result = {}
    for key, value in population_data.items():
        text = value.get("text", "")
        if not text:
            continue

        match = re.match(r'([\d,]+)\s*(\(.*\))?', text)
        if match:
            result[key] = {
                "value": int(match.group(1).replace(",", "")),
                "note": clean_text(match.group(2)) if match.group(2) else ""
            }
    return result


# Example usage
if __name__ == "__main__":
    population_data = {
        "total": {
            "text": "341,963,408"
        },
        "male": {
            "text": "168,598,780"
        },
        "female": {
            "text": "173,364,628 (2024 est.)"
        }
    }
    parsed_data = parse_population(population_data)
    print(parsed_data)
