######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import re
import logging

# ---------------------------------------------------------------------------------------------------------------------
# Import helper functions from the __worker_utils directory
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# ---------------------------------------------------------------------------------------------------------------------


def parse_major_rivers(major_rivers_data: dict, iso3Code: str = None) -> dict:
    """
    Parses the 'Major rivers' data for world ('WLD') specifically.

    Parameters:
        major_rivers_data (dict): The 'Major rivers' section from the data.

    Returns:
        dict: A dictionary containing parsed major rivers details, categorized by river details and specific notes.
    """
    result = {
        "major_rivers": [],
        "notes": []
    }

    # Extract the text content for major rivers
    text = major_rivers_data.get('text', '')
    if text:
        # Remove opening and closing <p> tags
        text = text.replace('<p>', '').replace('</p>', '')

        # Split the text at each semicolon
        entries = text.split(';')

        for entry in entries:
            entry = entry.strip()

            # Check if the entry is a note
            if entry.lower().startswith("note"):
                result["notes"].append(entry)
                continue

            # Extract river details: name, countries, length, and unit
            match = re.match(
                r'([^(]+)\s*\(([^)]+)\)\s*-\s*([\d,\.]+)\s*(km)', entry)
            if match:
                river_name = match.group(1).strip()
                countries = [country.strip()
                             for country in match.group(2).split(',')]
                length = float(match.group(3).replace(',', ''))
                unit = match.group(4).strip()

                # Determine if the river source or mouth is shared
                shared_info = []
                for country in countries:
                    if 'shared with' in country:
                        country_name = country.split('with')[-1].strip()
                        if '[s]' in country:
                            shared_info.append({'country': country_name.replace(
                                '[s]', '').strip(), 'type': 'source'})
                        elif '[m]' in country:
                            shared_info.append({'country': country_name.replace(
                                '[m]', '').strip(), 'type': 'mouth'})
                        else:
                            shared_info.append(
                                {'country': country_name, 'type': 'shared'})
                    else:
                        shared_info.append(
                            {'country': country, 'type': 'shared'})

                river_entry = {
                    'river_name': river_name,
                    'length': length,
                    'unit': unit,
                    'shared_with': shared_info
                }

                result["major_rivers"].append(river_entry)

    return result


def parse_wld_major_rivers(major_rivers_data: dict) -> dict:
    """
    Parses the 'Major rivers' data for world ('WLD') specifically.

    Parameters:
        major_rivers_data (dict): The 'Major rivers' section from the data.

    Returns:
        dict: A dictionary containing parsed major rivers details, categorized by river details and specific notes.
    """
    result = {
        "top_ten_longest_rivers": [],
        "notes": []
    }

    # Extract the text content for major rivers
    text = major_rivers_data.get('text', '')
    if text:
        # Split the text at the "<br><br>" to separate rivers and notes
        sections = text.split('<br><br>')

        # Process the first section containing the top ten longest rivers
        if sections:
            rivers_text = sections[0]
            if "top ten longest rivers:" in rivers_text.lower():
                rivers_text = rivers_text.split(
                    "top ten longest rivers:")[1].strip()
                river_entries = rivers_text.split(';')

                for entry in river_entries:
                    entry = entry.strip()
                    if entry:
                        # Extract river details: name, continent, length, and unit
                        match = re.match(
                            r'([^\(]+)\s*\(([^\)]+)\)\s*(\d+[\d,]*)\s*(km)', entry)
                        if match:
                            river_name = match.group(1).strip()
                            continent = match.group(2).strip()
                            length = float(match.group(3).replace(',', ''))
                            unit = match.group(4).strip()

                            river_entry = {
                                'river_name': river_name,
                                'continent': continent,
                                'length': length,
                                'unit': unit
                            }

                            result["top_ten_longest_rivers"].append(
                                river_entry)

        # Process the remaining sections containing notes
        for section in sections[1:]:
            note_match = re.match(
                r'<strong>note\s*\d*:</strong>\s*(.*)', section, re.IGNORECASE)
            if note_match:
                note_text = note_match.group(1).strip()
                result["notes"].append(note_text)

    return result


# Example usage
if __name__ == "__main__":
    """
    major_rivers_data = {
        "text": "<p>Missouri - 3,768 km; Mississippi - 3,544 km; Yukon river mouth (shared with Canada [s]) - 3,190 km; Saint Lawrence (shared with Canada) - 3,058 km; Rio Grande river source ( mouth shared with Mexico) - 3,057 km; Colorado river source (shared with Mexico [m]) - 2,333 km; Arkansas - 2,348 km; Columbia river mouth (shared with Canada [s]) - 2,250 km; Red - 2,188 km; Ohio - 2,102 km; Snake - 1,670 km<br><strong>note</strong> – [s] after country name indicates river source; [m] after country name indicates river mouth</p>"
    }
    print(parse_major_rivers(major_rivers_data))    
    """
    major_rivers_data = {
        "text": "<strong>top ten longest rivers:</strong> Nile (Africa) 6,650 km; Amazon (South America) 6,436 km; Yangtze (Asia) 6,300 km; Mississippi-Missouri (North America) 6,275 km; Yenisey-Angara (Asia) 5,539 km; Huang He/Yellow (Asia) 5,464 km; Ob-Irtysh (Asia) 5,410 km; Congo (Africa) 4,700 km; Amur (Asia) 4,444 km; Lena (Asia) 4,400 km<br><br><strong>note:</strong> there are 21 countries without rivers: three in Africa (Comoros, Djibouti, Libya), one in the Americas (Bahamas), eight in Asia (Bahrain, Kuwait, Maldives, Oman, Qatar, Saudi Arabia, United Arab Emirates, Yemen), three in Europe (Malta, Monaco, Holy See), and six in Oceania (Kiribati, Marshall Islands, Nauru, Niue, Tonga, Tuvalu); these countries also do not have natural lakes"
    }
    print(parse_wld_major_rivers(major_rivers_data))
