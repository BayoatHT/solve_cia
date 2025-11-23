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


def parse_land_use(land_use_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Land use' data.

    Parameters:
        land_use_data (dict): The 'Land use' section from the data.

    Returns:
        dict: A dictionary containing parsed land use details, including percentage, unit, and estimated year.
    """
    result = {}

    for key, value in land_use_data.items():
        # Extract the text content
        text = value.get('text', '')
        text = text.replace('agricultural land: ', '').replace('arable land: ', '').replace(
            'permanent crops: ', '').replace('permanent pasture: ', '').strip()

        if text:
            # Clean the text to remove any unwanted HTML or extra whitespace
            cleaned_text = clean_text(text)

            # Match pattern to extract value, unit, and estimated year
            match = re.match(r'([\d\.]+)%\s*\((\d{4})\s*est\.\)', cleaned_text)
            if match:
                percentage = float(match.group(1))
                est_year = int(match.group(2))

                # Rename keys as per requirements
                clean_key = key.lower()
                if clean_key == "agricultural land: arable land":
                    clean_key = clean_key.replace(
                        'agricultural land: arable land', 'arable_agricultural_land')
                elif clean_key == "agricultural land: permanent crops":
                    clean_key = clean_key.replace(
                        'agricultural land: permanent crops', 'permanent_crops_agricultural_land')
                elif clean_key == "agricultural land: permanent pasture":
                    clean_key = clean_key.replace(
                        'agricultural land: permanent pasture', 'permanent_pasture_agricultural_land')
                elif clean_key == "forest":
                    clean_key = clean_key.replace(
                        'forest', 'forest_agricultural_land')
                elif clean_key == "other":
                    clean_key = clean_key.replace(
                        'other', 'other_agricultural_land')
                elif clean_key == "agricultural land":
                    clean_key = clean_key.replace(
                        'agricultural land', 'agricultural_land')

                # Store parsed data in the result dictionary
                result[clean_key] = {
                    'percentage': percentage,
                    'unit': '%',
                    'est_year': est_year
                }
            else:
                # If matching fails, store the raw text
                result[key] = {'raw_text': cleaned_text}
        else:
            # If no text available, store an empty dictionary
            result[key] = {}

    return result
