import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_personnel(military_personnel_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'military personnel' data by splitting at semicolons not within parentheses.

    Parameters:
        military_personnel_data (dict): Dictionary containing the 'text' field with personnel data.

    Returns:
        dict: Structured dictionary with each segment as a separate entry in a list.
    """
    result = {
        "personnel_details": []
    }

    # Extract and clean text
    text = military_personnel_data.get("text", "")
    if not text:
        return result

    # Split by semicolons not inside parentheses
    parts = re.split(r';(?![^()]*\))', text)

    # Add each part as a cleaned-up entry in personnel_details
    for part in parts:
        result["personnel_details"].append(part.strip())

    return result


# Example usage
if __name__ == "__main__":
    military_personnel_data = {
        "text": "approximately 1.31 million active-duty personnel (446,000 Army; 328,000 Navy; 317,000 Air Force; 9,000 Space Force; 167,000 Marine Corps; 40,000 Coast Guard); 330,000 Army National Guard; 105,000 Air National Guard (2024)"
    }
    parsed_data = parse_military_personnel(military_personnel_data)
    print(parsed_data)
