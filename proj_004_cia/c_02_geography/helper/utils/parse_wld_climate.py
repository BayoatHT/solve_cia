
######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
# --------------------import logging----------------------------------------------------------------------------------------------


# Example usage for world climate data:
# parsed_climate = parse_wld_climate(data.get('Geography', {}).get('Climate', {}), 'WLD')
# print(parsed_climate)


def parse_wld_climate(climate_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Climate' data for world ('WLD') specifically.

    Parameters:
        climate_data (dict): The 'Climate' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        dict: A dictionary containing climate details, including general climate information, 
              as well as ten driest, wettest, coldest, and hottest places.
    """
    if return_original:
        return climate_data

    result = {}

    # Extract the general climate information
    general_climate = climate_data.get('Climate', {}).get('text', '')
    if general_climate:
        result['general_climate'] = clean_text(general_climate)
    else:
        result['general_climate'] = ''

    # Extract specific climate extremes (driest, wettest, coldest, hottest places)
    climate_extremes_keys = [
        'ten driest places on Earth (average annual precipitation)',
        'ten wettest places on Earth (average annual precipitation)',
        'ten coldest places on Earth (lowest average monthly temperature)',
        'ten hottest places on Earth (highest average monthly temperature)'
    ]

    for key in climate_extremes_keys:
        extreme_data = climate_data.get(key, {}).get('text', '')
        if extreme_data:
            # Split the data by <br> tags to get individual entries
            entries = extreme_data.split('<br>')

            # Parse each entry into a structured format
            parsed_entries = []
            for entry in entries:
                entry = entry.strip()
                if entry:
                    if key == 'ten driest places on Earth (average annual precipitation)':
                        # Match pattern for driest: 'Location, Country value mm (value in)'
                        match = re.match(
                            r'^(.*?),\s*(.*?)\s+([\d\.]+)\s*mm\s+\(([\d\.]+)\s*in\)$', entry)
                        if match:
                            location = match.group(1).strip()
                            country = match.group(2).strip()
                            mm_precipitation = float(match.group(3).strip())
                            in_precipitation = float(match.group(4).strip())

                            parsed_entries.append({
                                'location': location,
                                'country': country,
                                'mm_precipitation': mm_precipitation,
                                'in_precipitation': in_precipitation
                            })
                    elif key == 'ten wettest places on Earth (average annual precipitation)':
                        # Match pattern for wettest: 'Location, Country value mm (value in)'
                        match = re.match(
                            r'^(.*?),\s*(.*?)\s+([\d,\.]+)\s*mm\s+\(([\d\.]+)\s*in\)$', entry)
                        if match:
                            location = match.group(1).strip()
                            country = match.group(2).strip()
                            mm_precipitation = float(
                                match.group(3).replace(',', '').strip())
                            in_precipitation = float(match.group(4).strip())

                            parsed_entries.append({
                                'location': location,
                                'country': country,
                                'mm_precipitation': mm_precipitation,
                                'in_precipitation': in_precipitation
                            })
                    elif key == 'ten coldest places on Earth (lowest average monthly temperature)':
                        # Match pattern for coldest: 'Location, Country value°C (value°F) Month'
                        match = re.match(
                            r'^(.*?),\s*(.*?)\s+([-+]?\d+\.?\d*)°C\s+\((-?\d+\.?\d*)°F\)\s+(\w+)$', entry)
                        if match:
                            location = match.group(1).strip()
                            country = match.group(2).strip()
                            celsius = float(match.group(3).strip())
                            fahrenheit = float(match.group(4).strip())
                            month = match.group(5).strip()

                            parsed_entries.append({
                                'location': location,
                                'country': country,
                                'celsius': celsius,
                                'fahrenheit': fahrenheit,
                                'month': month
                            })
                    elif key == 'ten hottest places on Earth (highest average monthly temperature)':
                        # Match pattern for hottest: 'Location, Country value°C (value°F) Month'
                        match = re.match(
                            r'^(.*?),\s*(.*?)\s+([\d\.]+)°C\s+\(([\d\.]+)°F\)\s+(\w+)$', entry)
                        if match:
                            location = match.group(1).strip()
                            country = match.group(2).strip()
                            celsius = float(match.group(3).strip())
                            fahrenheit = float(match.group(4).strip())
                            month = match.group(5).strip()

                            parsed_entries.append({
                                'location': location,
                                'country': country,
                                'celsius': celsius,
                                'fahrenheit': fahrenheit,
                                'month': month
                            })
                    else:
                        # If no match, add the raw entry
                        parsed_entries.append({'raw_entry': entry})

            # Add the parsed entries to the result
            result[key.replace(' ', '_').lower()] = parsed_entries
        else:
            # If no data is available, return an empty list
            result[key.replace(' ', '_').lower()] = []

    return result
