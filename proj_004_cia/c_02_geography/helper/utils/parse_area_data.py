import re
import logging


def parse_area_data(area_data: dict, iso3Code: str=None, return_original: bool = False)-> dict:
    """
    Parses the 'Area' data into a dictionary containing numerical value, unit, and notes.

    Parameters:
        area_data (dict): The 'Area' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict: A dictionary containing area information with fields for value, unit, and notes.
               Ensures that `None` values are avoided by returning `0` or an empty string as appropriate.
    """
    if return_original:
        return area_data

    try:
        text = area_data.get('text', '')
        if not text:
            logging.warning(f"No text in 'Area' data for {iso3Code}")
            return {
                'value': 0,
                'unit': '',
                'notes': ''
            }

        # Clean HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Default values in case extraction fails
        area_info = {
            'value': 0,
            'unit': 'sq km',  # Set a default unit if none found
            'notes': ''
        }

        # Extract numerical value, unit, and optional notes
        match = re.match(r"([\d,]+)\s*(sq\s*km)?(?:\s*;\s*(.*))?", text)
        if match:
            # Convert numerical value, defaulting to 0 if parsing fails
            area_info['value'] = int(match.group(1).replace(
                ',', '')) if match.group(1) else 0
            # Default to 'sq km' if unit is missing
            area_info['unit'] = match.group(2) or 'sq km'
            # Default to empty string for notes
            area_info['notes'] = match.group(3) or ''

        return area_info

    except Exception as e:
        logging.error(f"Error parsing 'Area' for {iso3Code}: {e}")
        return {
            'value': 0,
            'unit': '',
            'notes': ''
        }
