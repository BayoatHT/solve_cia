######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# ------------------------------------------------------------------------------------------------------------------


def parse_map_references(map_ref_data: dict, isoCode: str = None):
    """
    Parses the 'Map references' data.

    Parameters:
        map_ref_data (dict): The 'Map references' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict or None: A dictionary mapping regions to their map references, or None if parsing fails.
    """
    try:
        text = map_ref_data.get('text', '')
        if not text:
            logging.warning(f"No text in 'Map references' data for {isoCode}")
            return {}

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Split the text into segments
        # Handle semicolons and line breaks
        segments = re.split(r';\s*', text)

        map_references_info = {}

        for segment in segments:
            segment = segment.strip()
            if segment:
                # Match patterns like 'metropolitan France: Europe'
                match = re.match(r'^(.*?):\s*(.*)$', segment)
                if match:
                    region = match.group(1).strip()
                    map_ref = match.group(2).strip()
                    map_references_info[region] = map_ref
                else:
                    # If there's no label, use a default key
                    map_references_info['map_reference'] = segment

        return map_references_info

    except Exception as e:
        logging.error(f"Error parsing 'Map references' for {isoCode}: {e}")
        return {}
