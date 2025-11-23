######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# ------------------------------------------------------------------------------------------------------------------


def parse_geographic_coordinates(
    coordinates_data: dict,
    iso3Code: str = None
):
    """
    Parses the 'Geographic coordinates' data.

    Parameters:
        coordinates_data (dict): The 'Geographic coordinates' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict or None: A dictionary mapping regions to their coordinates, or None if parsing fails.
    """
    try:
        text = coordinates_data.get('text', '')
        if not text:
            logging.warning(
                f"No text in 'Geographic coordinates' data for {iso3Code}")
            return {}

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Split the text into segments
        # Handle semicolons and line breaks
        segments = re.split(r';\s*', text)

        coordinates_info = {}

        for segment in segments:
            segment = segment.strip()
            if segment:
                # Match patterns like 'metropolitan France: 46 00 N, 2 00 E'
                match = re.match(r'^(.*?):\s*(.*)$', segment)
                if match:
                    region = match.group(1).strip()
                    coords = match.group(2).strip()
                    coordinates_info[region] = coords
                else:
                    # If there's no label, use a default key
                    coordinates_info['coordinates'] = segment

        return coordinates_info

    except Exception as e:
        logging.error(
            f"Error parsing 'Geographic coordinates' for {iso3Code}: {e}")
        return {}
