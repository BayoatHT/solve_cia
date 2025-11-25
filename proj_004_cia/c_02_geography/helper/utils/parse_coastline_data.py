######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from proj_004_cia.c_00_transform_utils.extract_numeric_value import extract_numeric_value
# ------------------------------------------------------------------------------------------------------------------


def parse_coastline_data(coastline_data, iso3Code: str = None, return_original: bool = False):
    """
    Parses the 'Coastline' data.

    Parameters:
        coastline_data (dict): The 'Coastline' data from the 'Geography' section.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict: A dictionary containing coastline length and note if available.
    """
    if return_original:
        return coastline_data

    result = {
        'value': 0,
        'unit': '',
        'note': ''
    }

    # Process 'text'
    text = coastline_data.get('text', '')
    if text:
        match = re.match(r'([\d,\.]+)\s*(\w+)', text)
        if match:
            result['value'] = extract_numeric_value(
                match.group(1), unit=match.group(2), iso3Code=iso3Code)
            result['unit'] = match.group(2)

    # Process 'note'
    note_data = coastline_data.get('note', '')
    if note_data:
        result['note'] = re.sub(r'<[^>]+>', '', note_data)

    return result
