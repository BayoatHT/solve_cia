######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
# ------------------------------------------------------------------------------------------------------------------



def parse_area_comparative(area_comparative_data: dict, iso3Code: str=None) -> str:
    
    """
    Parses the 'Area - comparative' data into a cleaned string.

    Parameters:
        area_comparative_data (dict): The 'Area - comparative' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        str: A cleaned string representing the comparative area information.
    """
    try:
        text = area_comparative_data.get('text', '')
        if not text:
            logging.warning(
                f"No text in 'Area - comparative' data for {iso3Code}")
            return ''

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    except Exception as e:
        logging.error(
            f"Error parsing 'Area - comparative' for {iso3Code}: {e}")
        return ''
