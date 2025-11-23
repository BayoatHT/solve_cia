######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.extract_numeric_value import extract_numeric_value
# ------------------------------------------------------------------------------------------------------------------


def parse_land_boundaries_master(land_boundaries_data, iso3Code: str = None):
    """
    Parses the entire 'Land boundaries' section.

    Parameters:
        land_boundaries_data (dict): The 'Land boundaries' data from the 'Geography' section.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict: A dictionary containing total land boundaries, border countries, notes, and any other territories.
    """
    result = {
        'total': {'value': 0, 'unit': ''},
        'border_countries': [],
        'notes': '',
        'territories': {}
    }

    # Process 'total'
    total_data = land_boundaries_data.get('total', {})
    total_text = total_data.get('text', '')
    if total_text:
        match = re.match(r'([\d,\.]+)\s*(\w+)', total_text)
        if match:
            result['total'] = {
                'value': extract_numeric_value(match.group(1), unit=match.group(2), iso3Code=iso3Code),
                'unit': match.group(2)
            }

    # Process 'border countries'
    border_data = land_boundaries_data.get('border countries', {})
    border_text = border_data.get('text', '')
    if border_text:
        border_text = re.sub(r'<[^>]+>', '', border_text)
        segments = re.split(r';\s*', border_text)
        for segment in segments:
            segment = segment.strip()
            if segment:
                match = re.match(
                    r'^(.*?)\s([\d,\.]+)\s*(\w+)(?:\s*\((.*?)\))?$', segment)
                if match:
                    border_country = match.group(1).strip()
                    value = extract_numeric_value(match.group(
                        2), unit=match.group(3), iso3Code=iso3Code)
                    unit = match.group(3).strip()
                    note = match.group(4).strip() if match.group(4) else ""
                    result['border_countries'].append({
                        'border_country': border_country,
                        'value': value,
                        'unit': unit,
                        'note': note
                    })

    # Process 'note'
    note_data = land_boundaries_data.get('note', '')
    if note_data:
        result['notes'] = re.sub(r'<[^>]+>', '', note_data)

    # Process other territories (e.g., 'metropolitan France - total', 'French Guiana - total')
    for key, value in land_boundaries_data.items():
        if key not in ['total', 'border countries', 'note']:
            territory_text = value.get('text', '')
            if territory_text:
                match = re.match(r'([\d,\.]+)\s*(\w+)', territory_text)
                if match:
                    result['territories'][key] = {
                        'value': extract_numeric_value(match.group(1), unit=match.group(2), iso3Code=iso3Code),
                        'unit': match.group(2)
                    }

    return result
