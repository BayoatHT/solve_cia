import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_location(location_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """

    """
    if return_original:
        return location_data

    if not location_data:
        logging.warning(f"No 'Location' data found for {iso3Code}")
        return None

    text = location_data.get('text', '')
    if not text:
        logging.warning(f"No text in 'Location' data for {iso3Code}")
        return None

    # Remove HTML tags from the text
    text = re.sub(r'<[^>]+>', '', text)

    # Initialize a dictionary to hold location information
    location_info = {}

    # Initialize a flag to check if labels are present
    has_labels = False

    # Split the text into segments based on semicolons
    segments = text.split(';')

    for segment in segments:
        segment = segment.strip()
        if segment:
            # Check if the segment contains a label followed by a colon
            match = re.match(r'\s*(.*?)\s*:\s*(.*)', segment)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                location_info[key] = value
                has_labels = True
            else:
                # If no label is found, add the segment under 'description'
                if 'description' in location_info:
                    location_info['description'] += ' ' + segment
                else:
                    location_info['description'] = segment

    # If labels were found, return the location_info dictionary
    if has_labels:
        return location_info
    else:
        # If no labels, return the 'description' string
        return location_info.get('description', '')


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------------------------
    location_data = {

    }
    isoCode = 'USA'
    parsed_data = parse_location(location_data, isoCode)
    print(parsed_data)
