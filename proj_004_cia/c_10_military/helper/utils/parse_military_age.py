import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def split_notes(note_text: str) -> list:
    """
    Splits a note text into individual notes based on <br><br> tags,
    and removes <strong> tags and any content inside them.

    Parameters:
        note_text (str): The raw note text to be split.

    Returns:
        list: A list of cleaned notes.
    """
    # Split the text into parts at <br><br> tags
    parts = note_text.split('<br><br>')
    # Clean each part by removing <strong> tags and their content
    cleaned_notes = [clean_text(re.sub(r'<strong>.*?</strong>', '', part, flags=re.IGNORECASE))
                     for part in parts if part.strip()]
    return cleaned_notes


def parse_military_age(military_age_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to military age requirements and associated notes.

    Parameters:
        military_age_data (dict): The dictionary containing military age data.

    Returns:
        dict: A dictionary containing parsed information for military age requirements and notes.
    """
    result = {
        "mil_age": [],
        "mil_age_notes": []
    }

    # Handle 'text'
    age_text = military_age_data.get("text", "")
    if age_text:
        result["mil_age"] = parse_text_to_list(age_text)

    # Handle 'note'
    age_note = military_age_data.get("note", "")
    if age_note:
        result["mil_age_notes"] = split_notes(age_note)

    return result


# Example usage
if __name__ == "__main__":
    # Example data with multiple notes
    military_age_data = {
        "text": "18 years of age (17 years of age with parental consent) for voluntary service for men and women; no conscription (currently inactive, but males aged 18-25 must register with Selective Service in case conscription is reinstated in the future); maximum enlistment age 34 (Army), 42 (Air Force/Space Force), 39 (Navy), 28 (Marines), 31 (Coast Guard); 8-year service obligation, including 2-5 years active duty (Army), 2 years active duty (Navy), 4 years active duty (Air Force, Coast Guard, Marines, Space Force) (2023)",
        "note": "<strong>note 1: </strong>the US military has been all-volunteer since 1973, but an act of Congress can reinstate the draft in case of a national emergency<strong><br><br>note 2:</strong> all military occupations and positions open to women; in 2021, women comprised over 17% of the total US active duty military personnel; a small number of American women were involved in combat during the Revolutionary (1775-1783), Mexican (1846-1848), and Civil (1861-1865) Wars, but they had to disguise themselves as men and enlist under aliases; the first official US military organization for women was the US Army Nurse Corps, established in 1901; during World War I, the US Navy and Marine Corps allowed women to enlist; nearly 350,000 women served in the US military during World War II; the 1991 Gulf War was the first war where women served with men in integrated units within a war zone; in 2015, women were allowed to serve in direct combat roles<br><br><strong>note 3:</strong> non-citizens living permanently and legally in the US may join as enlisted personnel; must have permission to work in the US, a high school diploma, and speak, read, and write English fluently; minimum age of 17 with parental consent or 18 without; maximum age 29-39, depending on the service; under the US Nationality Act, honorable service in the military may qualify individuals to obtain expedited citizenship; under the Compact of Free Association, citizens of the Federated States of Micronesia, the Republic of Palau, and the Republic of the Marshall Islands may volunteer; under the Jay Treaty, signed in 1794 between Great Britain and the US, and corresponding legislation, Native Americans/First Nations born in Canada are entitled to freely enter the US and join the US military"
    }
    parsed_data = parse_military_age(military_age_data)
    print(parsed_data)
