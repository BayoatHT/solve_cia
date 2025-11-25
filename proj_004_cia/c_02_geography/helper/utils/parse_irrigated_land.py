######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import re
import logging

# ---------------------------------------------------------------------------------------------------------------------
# Import helper functions from the __worker_utils directory
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------------------------------------------------------------------------------------------------------


def parse_irrigated_land(irrigated_land_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Irrigated land' data.

    Parameters:
        irrigated_land_data (dict): The 'Irrigated land' section from the data.

    Returns:
        dict: A dictionary containing parsed irrigated land details, including area, unit, and estimated year.
    """
    if return_original:
        return irrigated_land_data

    result = {}

    # Extract the text content
    text = irrigated_land_data.get('text', '')
    if text:
        # Clean the text to remove any unwanted HTML or extra whitespace
        cleaned_text = clean_text(text)

        # Match pattern to extract value, unit, and estimated year
        match = re.match(
            r'([\d,\.]+)\s*sq km\s*\(?((\d{4})(?:\s*est\.)?)?\)?', cleaned_text)
        if match:
            value = float(match.group(1).replace(',', ''))
            est_year = int(match.group(3)) if match.group(3) else None

            # Store parsed data in the result dictionary
            result = {
                'value': value,
                'unit': 'sq km',
                'est_year': est_year
            }
        else:
            # If matching fails, store the raw text
            result = {'raw_text': cleaned_text}
    else:
        # If no text available, store an empty dictionary
        result = {}

    return result
