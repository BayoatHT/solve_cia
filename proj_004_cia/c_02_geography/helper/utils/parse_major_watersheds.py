######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import re
import logging

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------------------------------------------------------------------------------------------------------


def parse_major_watersheds(major_watersheds_data: dict, iso3Code: str=None) -> dict:
    """
    Parses the 'Major watersheds' data for specific countries.

    Parameters:
        major_watersheds_data (dict): The 'Major watersheds' section from the data.

    Returns:
        dict: A dictionary containing parsed major watersheds details, organized by ocean/sea drainage and related rivers.
    """
    result = {
        "watersheds": []
    }

    # Extract the text content for major watersheds
    text = major_watersheds_data.get('text', '')
    if text:
        # Remove <em> tags and any surrounding whitespace
        text = re.sub(r'<em>|</em>', '', text).strip()

        # Split the text by line breaks to separate different watersheds and their rivers
        watershed_entries = re.split(r'<br>', text)

        for entry in watershed_entries:
            entry = entry.strip()
            if entry:
                # Split the entry by colons to separate drainage basins from rivers
                parts = entry.split(':', 1)
                if len(parts) == 2:
                    current_ocean = parts[0].strip()
                    rivers_text = parts[1].strip()

                    # Split rivers by semicolon to get individual river entries
                    river_entries = re.split(r';', rivers_text)
                    for river_entry in river_entries:
                        river_entry = river_entry.strip()
                        if river_entry:
                            # Match river name and area
                            match = re.match(
                                r'([^(]+)\s*\(([^)]+)\)', river_entry)
                            if match:
                                river_name = match.group(1).strip()
                                area_info = match.group(2).strip()

                                # Split area information to extract area and US only area if present
                                area_parts = area_info.split(',')
                                area = float(area_parts[0].replace(
                                    ',', '').split()[0])
                                unit = "sq km"

                                us_only_area = None
                                if len(area_parts) > 1 and 'US only' in area_parts[1]:
                                    us_only_area = float(area_parts[1].replace(
                                        'US only', '').replace(',', '').split()[0])

                                # Add the parsed river entry to the result
                                river_data = {
                                    'river_name': river_name,
                                    'drainage': current_ocean,
                                    'area': area,
                                    'unit': unit
                                }

                                if us_only_area:
                                    river_data['us_only_area'] = us_only_area

                                # Check if the river has a source or mouth indication
                                if '[s]' in river_name:
                                    river_data['source'] = True
                                    river_name = river_name.replace(
                                        '[s]', '').strip()
                                if '[m]' in river_name:
                                    river_data['mouth'] = True
                                    river_name = river_name.replace(
                                        '[m]', '').strip()

                                river_data['river_name'] = river_name
                                result["watersheds"].append(river_data)

    return result


# Example usage
if __name__ == "__main__":
    major_watersheds_data = {
        "text": "Atlantic Ocean drainage: <em>(Gulf of Mexico) </em>Mississippi* (3,202,185 sq km); Rio Grande (607,965 sq km); <em>(Gulf of Saint Lawrence)</em> Saint Lawrence* (1,049,636 sq km total, US only 505,000 sq km)<br>Pacific Ocean drainage: Yukon* (847,620 sq km, US only 23,820 sq km); Colorado (703,148 sq km); Columbia* (657,501 sq km, US only 554,501 sq km)<br>note - watersheds shared with Canada shown with *"
    }
    print(parse_major_watersheds(major_watersheds_data))
