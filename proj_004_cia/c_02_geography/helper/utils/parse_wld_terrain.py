######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# ------------------------------------------------------------------------------------------------------------------


def parse_wld_terrain(terrain_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Terrain' data for world ('WLD') specifically.

    Parameters:
        terrain_data (dict): The 'Terrain' section from the data.

    Returns:
        dict: A dictionary containing general terrain details, as well as detailed cave information.
    """
    result = {}

    # Extract general terrain information
    general_terrain = terrain_data.get('Terrain', {}).get('text', '')
    if general_terrain:
        result['general_terrain'] = clean_text(general_terrain)
    else:
        result['general_terrain'] = ''

    # Extract specific information about the top ten caves
    top_ten_caves = terrain_data.get('Top ten world caves', {}).get('text', '')
    if top_ten_caves:
        # Split the data by <br><br> tags to get individual cave entries
        entries = top_ten_caves.split('<br><br>')

        parsed_entries = []
        for entry in entries:
            entry = entry.strip()
            if entry:
                # Match pattern: '<em>cave_type:</em> description'
                match = re.match(r'<em>([^:]+):</em>\s*(.*)', entry)
                if match:
                    cave_type = match.group(1).strip().replace(
                        '<strong>', '').replace('</strong>', '')
                    description = clean_text(match.group(2).strip())
                    parsed_entries.append({
                        'cave_type': cave_type,
                        'description': description
                    })

        # Add the parsed entries to the result
        result['top_ten_world_caves'] = parsed_entries
    else:
        # If no data is available, return an empty list
        result['top_ten_world_caves'] = []

    return result
