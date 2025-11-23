import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_communications_note(communications_note_data: dict) -> dict:
    """

    """

    result = {}

    return result


# Example usage
if __name__ == "__main__":
    communications_note_data = {
        "text": "<strong>note 1:</strong> The Library of Congress, Washington DC, USA, claims to be the largest library in the world with more than 167 million items (as of 2018); its collections are universal, not limited by subject, format, or national boundary, and include materials from all parts of the world and in over 450 languages; collections include: books, newspapers, magazines, sheet music, sound and video recordings, photographic images, artwork, architectural drawings, and copyright data<br><br><strong>note 2:</strong> Cape Canaveral, Florida, USA, hosts one of four dedicated ground antennas that assist in the operation of the Global Positioning System (GPS) navigation system (the others are on Ascension (Saint Helena, Ascension, and Tistan da Cunha), Diego Garcia (British Indian Ocean Territory), and at Kwajalein (Marshall Islands)"
    }
    parsed_data = parse_communications_note(communications_note_data)
    print(parsed_data)
