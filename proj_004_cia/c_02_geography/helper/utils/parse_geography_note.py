import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_geography_note(geography_note_data: dict, iso3Code: str = None, return_original: bool = False)-> dict:
    """
    Parses the 'Geography - note' data for a country.

    Parameters:
        geography_note_data (dict): The 'Geography - note' section from the data.

    Returns:
        dict: A dictionary containing parsed details of geography notes.
    """
    if return_original:
        return geography_note_data

    result = {}

    text = geography_note_data.get("text", "")
    if not text:
        return result

    # Split the text by paragraph tags to extract individual notes
    paragraphs = re.split(r'</?p>', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    for paragraph in paragraphs:
        # Extract the note number and content
        match = re.match(r'<strong>(note \d+):</strong>\s*(.*)', paragraph)
        if match:
            note_key = match.group(1).replace(" ", "_").lower()
            note_content = match.group(2)

            # Split the content into different parts by semicolons
            note_items = [item.strip()
                          for item in note_content.split(';') if item.strip()]
            result[note_key] = note_items

    return result


# Example usage
if __name__ == "__main__":
    geography_note_data = {
        "text": "<p><strong>note 1:</strong> world's third-largest country by size (after Russia and Canada) and by population (after China and India); Denali (Mt. McKinley) is the highest point (6,190 m) in North America and Death Valley the lowest point (-86 m) on the continent</p> <p><strong>note 2:</strong> the western coast of the United States and southern coast of Alaska lie along the Ring of Fire, a belt of active volcanoes and earthquake epicenters bordering the Pacific Ocean; up to 90% of the world's earthquakes and some 75% of the world's volcanoes occur within the Ring of Fire</p> <p><strong>note 3:</strong> the Aleutian Islands are a chain of volcanic islands that divide the Bering Sea (north) from the main Pacific Ocean (south); they extend about 1,800 km westward from the Alaskan Peninsula; the archipelago consists of 14 larger islands, 55 smaller islands, and hundreds of islets; there are 41 active volcanoes on the islands, which together form a large northern section of the Ring of Fire<br><br><strong>note 4: </strong>Mammoth Cave, in west-central Kentucky, is the world's longest known cave system with more than 650 km (405 miles) of surveyed passageways, which is nearly twice as long as the second-longest cave system, the Sac Actun underwater cave in Mexico -- the world's longest underwater cave system (see \"Geography - note\" under Mexico)</p><br><br><strong>note 5:</strong> Kazumura Cave on the island of Hawaii is the world's longest and deepest lava tube cave; it has been surveyed at 66 km (41 mi) long and 1,102 m (3,614 ft) deep"
    }
    parsed_data = parse_geography_note(geography_note_data)
    print(parsed_data)
