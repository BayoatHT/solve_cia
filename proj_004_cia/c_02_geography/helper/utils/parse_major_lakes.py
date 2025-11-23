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


def parse_major_lakes(major_lakes_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Major lakes' data.

    Parameters:
        major_lakes_data (dict): The 'Major lakes' section from the data.

    Returns:
        dict: A dictionary containing parsed major lakes details, categorized by fresh and salt water lakes.
    """
    result = {}

    for lake_type, lake_data in major_lakes_data.items():
        # Extract the text content for the current lake type (e.g., fresh water lake(s), salt water lake(s))
        text = lake_data.get('text', '')
        if text:
            # Clean the text to remove any unwanted HTML or extra whitespace
            cleaned_text = clean_text(text)

            # Replace asterisks (*) with " Lake"
            # cleaned_text = cleaned_text.replace('*', ' Lake')

            parsed_lakes = []

            if lake_type.lower() == 'salt water lake(s)':
                # Split the cleaned text by every second semicolon to separate different entries for salt water lakes
                lake_entries = cleaned_text.split(';')
                for i in range(0, len(lake_entries), 2):
                    if i + 1 < len(lake_entries):
                        lake_name = lake_entries[i].strip()
                        area_and_unit = lake_entries[i + 1].strip()

                        # Match pattern to extract area and unit
                        match = re.match(
                            r'([\d,\.]+)\s*(sq km)', area_and_unit)
                        if match:
                            area = float(match.group(1).replace(',', ''))
                            unit = match.group(2).strip()

                            parsed_lakes.append({
                                'lake_name': lake_name,
                                'area': area,
                                'unit': unit
                            })
                        else:
                            # If no match, store the raw entry
                            parsed_lakes.append(
                                {'raw_entry': f"{lake_name} - {area_and_unit}"})
            else:
                # Split the cleaned text by ';' to separate different entries for fresh water lakes
                lake_entries = cleaned_text.split(';')
                for entry in lake_entries:
                    entry = entry.strip()
                    if entry:
                        # Match pattern to extract lake name, area, and unit
                        match = re.match(
                            r'([^–\-]+)\s*[\u2013\-]\s*([\d,\.]+)\s*(sq km)', entry)
                        if match:
                            lake_name = match.group(1).strip()
                            area = float(match.group(2).replace(',', ''))
                            unit = match.group(3).strip()

                            parsed_lakes.append({
                                'lake_name': lake_name,
                                'area': area,
                                'unit': unit
                            })
                        else:
                            # If no match, store the raw entry
                            parsed_lakes.append({'raw_entry': entry})

            # Store parsed lakes under the corresponding lake type key
            clean_key = lake_type.lower().replace(' ', '_').replace('(', '').replace(')', '')
            result[clean_key] = parsed_lakes
        else:
            # If no text available, store an empty list
            result[lake_type] = []

    return result


def parse_wld_major_lakes(major_lakes_data: dict) -> dict:
    """
    Parses the 'Major lakes' data for world ('WLD') specifically.

    Parameters:
        major_lakes_data (dict): The 'Major lakes' section from the data.

    Returns:
        dict: A dictionary containing parsed major lakes details, categorized by natural lakes and specific notes.
    """
    result = {
        "top_ten_largest_natural_lakes": [],
        "notes": {}
    }

    # Extract the text content for major lakes
    text = major_lakes_data.get('text', '')
    if text:
        # Clean the text to remove any unwanted HTML or extra whitespace
        cleaned_text = clean_text(text)

        # Split the cleaned text by '<br><br>' to separate different sections
        sections = cleaned_text.split('<br><br>')
        for section in sections:
            section = section.strip()
            if section.startswith("<strong>"):
                # Extract the heading for the group of lakes or notes
                heading_match = re.match(r'<strong>([^:]+):</strong>', section)
                if heading_match:
                    current_note = heading_match.group(
                        1).strip().lower().replace(' ', '_')
                    result["notes"][current_note] = []
            else:
                # Extract lake details: name, countries, area, unit
                match = re.findall(
                    r'([^\(]+)\(([^\)]+)\)\s*([\d,\.]+)\s*(sq km)', section)
                if match:
                    for lake in match:
                        lake_name = lake[0].strip()
                        countries = [country.strip()
                                     for country in lake[1].split(',')]
                        area = float(lake[2].replace(',', ''))
                        unit = lake[3].strip()

                        lake_entry = {
                            'lake_name': lake_name.replace('; ', '').replace('top ten largest natural lakes: ', ''),
                            'countries': countries,
                            'area': area,
                            'unit': unit
                        }

                        result["top_ten_largest_natural_lakes"].append(
                            lake_entry)
                else:
                    # If no match, store the raw entry under the appropriate note
                    if current_note:
                        result["notes"][current_note].append(section)

    return result
