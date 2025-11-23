import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_forces(military_forces_data: dict, iso3Code: str = None) -> dict:
    """
    Parses 'Military Forces' data, extracting details on branches, abbreviations, and associated notes.

    Parameters:
        military_forces_data (dict): The 'Military Forces' section from the data.

    Returns:
        dict: A structured dictionary containing branches, abbreviations, metadata, and notes.
    """
    result = {
        "branches": [],
        "year": "",
        "military_note": []
    }

    # Extract and parse the main text information
    text = military_forces_data.get("text", "")
    if text:
        # Extract the year if present at the end
        year_match = re.search(r"\((\d{4})\)$", text)
        if year_match:
            result["year"] = year_match.group(1)
            # Remove the year part from the text
            text = text[:year_match.start()].strip()

        # Split by <br><br> or semicolons for branch information
        branches = re.split(r"(?:<br><br>|;)", text)

        # Process each branch chunk
        for branch in branches:
            branch_info = {
                "branch": clean_text(branch).strip()
            }
            result["branches"].append(branch_info)

    # Parse and clean up notes, dividing by <br><br> and removing <strong> tags
    note_text = military_forces_data.get("note", "")
    if note_text:
        notes = re.split(r"<br><br>", note_text)
        for note in notes:
            # Clean the HTML tags and strong tags, remove any numbering in strong tags
            clean_note = re.sub(
                r'<strong>note\s*\d*:\s*</strong>', '', note, flags=re.IGNORECASE)
            result["military_note"].append(clean_text(clean_note))

    return result


# Example usage
if __name__ == "__main__":
    military_forces_data = {
        "text": "United States Armed Forces (aka US Military): US Army (USA), US Navy (USN; includes US Marine Corps or USMC), US Air Force (USAF), US Space Force (USSF); US Coast Guard (USCG); National Guard (Army National Guard and Air National Guard) (2024)",
        "note": "<strong>note 1: </strong>the US Coast Guard is administered in peacetime by the Department of Homeland Security, but in wartime reports to the Department of the Navy<br><strong><br>note 2:</strong> the Army National Guard and the Air National Guard are reserve components of their services and operate in part under state authority; the US military also maintains reserve forces for each branch<br><br><strong>note 3: </strong>US law enforcement personnel include those of federal agencies, such as the Department of Homeland Security and Department of Justice, the 50 states, special jurisdictions, local sheriff’s offices, and municipal, county, regional, and tribal police departments<br><br><strong>note 4:</strong> the US has state defense forces (SDFs), which are military units that operate under the sole authority of state governments; SDFs are authorized by state and federal law and are under the command of the governor of each state; as of 2023, more than 20 states and the Commonwealth of Puerto Rico had SDFs, which typically have emergency management and homeland security missions; most are organized as ground units, but air and naval units also exist"
    }
    parsed_data = parse_military_forces(military_forces_data)
    print(parsed_data)
