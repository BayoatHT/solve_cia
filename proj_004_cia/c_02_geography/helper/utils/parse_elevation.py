######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# ---------------------------------------------------------------------------------------------------------------------

# Configure logging
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------------------------------------------------------------------------------------------------------


def parse_elevation(elevation_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Elevation' data for a given country.

    Parameters:
        elevation_data (dict): The 'Elevation' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict: A dictionary containing elevation details including highest point, lowest point, 
              mean elevation, and any additional notes.
    """
    if return_original:
        return elevation_data

    result = {}

    # Parse highest point
    highest_point = elevation_data.get('highest point', {}).get('text', '')
    if highest_point:
        match = re.match(r'^(.*?)([\d,\.]+)\s*(m|ft)?$', highest_point.strip())
        if match:
            location = match.group(1).strip()
            height = float(match.group(2).replace(',', '').strip())
            unit = match.group(3).strip() if match.group(
                3) else 'm'  # Default to meters if no unit provided

            result['highest_point'] = {
                'location': location,
                'height': height,
                'unit': unit
            }
        else:
            result['highest_point'] = {'raw_text': highest_point}
    else:
        result['highest_point'] = {}

    # Parse lowest point
    lowest_point = elevation_data.get('lowest point', {}).get('text', '')
    if lowest_point:
        match = re.match(r'^(.*?)([-\d,\.]+)\s*(m|ft)?$', lowest_point.strip())
        if match:
            location = match.group(1).strip()
            depth = float(match.group(2).replace(',', '').strip())
            unit = match.group(3).strip() if match.group(
                3) else 'm'  # Default to meters if no unit provided

            result['lowest_point'] = {
                'location': location,
                'depth': depth,
                'unit': unit
            }
        else:
            result['lowest_point'] = {'raw_text': lowest_point}
    else:
        result['lowest_point'] = {}

    # Parse mean elevation
    mean_elevation = elevation_data.get('mean elevation', {}).get('text', '')
    if mean_elevation:
        match = re.match(r'^([\d,\.]+)\s*(m|ft)?$', mean_elevation.strip())
        if match:
            elevation = float(match.group(1).replace(',', '').strip())
            unit = match.group(2).strip() if match.group(
                2) else 'm'  # Default to meters if no unit provided

            result['mean_elevation'] = {
                'elevation': elevation,
                'unit': unit
            }
        else:
            result['mean_elevation'] = {'raw_text': mean_elevation}
    else:
        result['mean_elevation'] = {}

    # Parse additional note
    note = elevation_data.get('note', '')
    if note:
        # Extract the note text using clean_text and BeautifulSoup
        cleaned_note = clean_text(note)
        result['note'] = cleaned_note
    else:
        result['note'] = ''

    return result


def parse_wld_elevation(elevation_data: dict, iso3Code: str, return_original: bool = False)-> dict:
    """
    Parses the 'Elevation' data for world ('WLD') specifically.

    Parameters:
        elevation_data (dict): The 'Elevation' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict: A dictionary containing elevation details, including highest point, lowest point,
              mean elevation, and detailed world-specific notes.
    """
    if return_original:
        return elevation_data

    result = {}

    # Parse highest point
    highest_point = elevation_data.get('highest point', {}).get('text', '')
    if highest_point:
        match = re.match(r'^(.*?)([\d,\.]+)\s*(m|ft)?$', highest_point.strip())
        if match:
            location = match.group(1).strip()
            height = float(match.group(2).replace(',', '').strip())
            unit = match.group(3).strip() if match.group(
                3) else 'm'  # Default to meters if no unit provided

            result['highest_point'] = {
                'location': location,
                'height': height,
                'unit': unit
            }
        else:
            result['highest_point'] = {'raw_text': highest_point}
    else:
        result['highest_point'] = {}

    # Parse lowest point
    lowest_point = elevation_data.get('lowest point', {}).get('text', '')
    if lowest_point:
        match = re.match(r'^(.*?)([-\d,\.]+)\s*(m|ft)?$', lowest_point.strip())
        if match:
            location = match.group(1).strip()
            depth = float(match.group(2).replace(',', '').strip())
            unit = match.group(3).strip() if match.group(
                3) else 'm'  # Default to meters if no unit provided

            result['lowest_point'] = {
                'location': location,
                'depth': depth,
                'unit': unit
            }
        else:
            result['lowest_point'] = {'raw_text': lowest_point}
    else:
        result['lowest_point'] = {}

    # Parse mean elevation
    mean_elevation = elevation_data.get('mean elevation', {}).get('text', '')
    if mean_elevation:
        match = re.match(r'^([\d,\.]+)\s*(m|ft)?$', mean_elevation.strip())
        if match:
            elevation = float(match.group(1).replace(',', '').strip())
            unit = match.group(2).strip() if match.group(
                2) else 'm'  # Default to meters if no unit provided

            result['mean_elevation'] = {
                'elevation': elevation,
                'unit': unit
            }
        else:
            result['mean_elevation'] = {'raw_text': mean_elevation}
    else:
        result['mean_elevation'] = {}

    # Parse additional note - world-specific parsing
    note = elevation_data.get('note', '')
    if note:
        cleaned_note = clean_text(note)
        parsed_notes = {}

        # Define and extract individual categories from the note
        categories = {
            'top_ten_highest_mountains': r'<strong>top ten highest mountains \(measured from sea level\):</strong>(.*?)(?=<strong>|$)',
            'top_ten_highest_island_peaks': r'<strong>top ten highest island peaks:</strong>(.*?)(?=<strong>|$)',
            'highest_point_on_each_continent': r'<strong>highest point on each continent:</strong>(.*?)(?=<strong>|$)',
            'highest_capital_on_each_continent': r'<strong>highest capital on each continent:</strong>(.*?)(?=<strong>|$)',
            'lowest_point_on_each_continent': r'<strong>lowest point on each continent:</strong>(.*?)(?=<strong>|$)',
            'lowest_capital_on_each_continent': r'<strong>lowest capital on each continent:</strong>(.*?)(?=<strong>|$)'
        }

        # Iterate over each category and parse the relevant entries
        for category, pattern in categories.items():
            match = re.search(pattern, note, re.DOTALL)

            if match:
                entries = match.group(1).strip()
                entry_list = entries.split('; ')
                parsed_entries = []

                for entry in entry_list:
                    entry = entry.strip()

                    # Parsing logic for different categories
                    if category in ['top_ten_highest_mountains', 'top_ten_highest_island_peaks']:
                        parsed_entry_match = re.match(
                            r'^(.*?)(\((.*?)\))?\s+([\d,\.]+)\s*m$', entry)
                        if parsed_entry_match:
                            name = parsed_entry_match.group(1).strip()
                            location = parsed_entry_match.group(
                                3).strip() if parsed_entry_match.group(3) else ''
                            height = float(parsed_entry_match.group(
                                4).replace(',', '').strip())
                            parsed_entries.append({
                                'name': name,
                                'location': location,
                                'height': height,
                                'unit': 'm'
                            })
                    elif category in ['highest_point_on_each_continent', 'lowest_point_on_each_continent']:
                        parsed_entry_match = re.match(
                            r'^(.*?)-\s*(.*)\s+([\d,\.]+)\s*m$', entry)
                        if parsed_entry_match:
                            continent = parsed_entry_match.group(1).strip()
                            name = parsed_entry_match.group(2).strip()
                            value = float(parsed_entry_match.group(
                                3).replace(',', '').strip())
                            parsed_entries.append({
                                'continent': continent,
                                'name': name,
                                'value': value,
                                'unit': 'm'
                            })
                    elif category in ['highest_capital_on_each_continent', 'lowest_capital_on_each_continent']:
                        parsed_entry_match = re.match(
                            r'^(.*?)-\s*(.*)\s+([\d,\.]+)\s*m$', entry)
                        if parsed_entry_match:
                            continent = parsed_entry_match.group(1).strip()
                            capital = parsed_entry_match.group(2).strip()
                            value = float(parsed_entry_match.group(
                                3).replace(',', '').strip())
                            parsed_entries.append({
                                'continent': continent,
                                'capital': capital,
                                'value': value,
                                'unit': 'm'
                            })

                # Add the parsed entries to the final dictionary
                parsed_notes[category] = parsed_entries

        result['note'] = parsed_notes
    else:
        result['note'] = {}

    return result
