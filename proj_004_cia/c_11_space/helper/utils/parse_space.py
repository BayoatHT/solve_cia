import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def parse_space(space_data: dict, iso3Code: str = None) -> dict:
    """
    Parses data related to space programs, agencies, and launch sites, including associated notes.

    Parameters:
        space_data (dict): The dictionary containing space data.

    Returns:
        dict: A dictionary containing parsed information for space agencies, launch sites, and an overview.
    """
    result = {
        "space_agencies": [],
        "space_agencies_note": "",
        "space_launch_sites": [],
        "space_launch_sites_note": [],
        "space_program_overview": [],
        "space_program_overview_note": ""
    }

    # Handle 'Space agency/agencies'
    agencies_data = space_data.get("Space agency/agencies", {})
    if agencies_data:
        # Handle 'text'
        agencies_text = agencies_data.get("text", "")
        if agencies_text:
            result["space_agencies"] = parse_text_to_list(agencies_text)

        # Handle 'note'
        agencies_note = agencies_data.get("note", "")
        if agencies_note:
            clean_agencies_note = re.sub(
                r'<strong>note:</strong>\s*', '', agencies_note, flags=re.IGNORECASE)
            result["space_agencies_note"] = clean_text(clean_agencies_note)

    # Handle 'Space launch site(s)'
    launch_sites_data = space_data.get("Space launch site(s)", {})
    if launch_sites_data:
        # Handle 'text'
        launch_sites_text = launch_sites_data.get("text", "")
        if launch_sites_text:
            result["space_launch_sites"] = parse_text_to_list(
                launch_sites_text)

        # Handle 'note'
        launch_sites_note = launch_sites_data.get("note", "")
        if launch_sites_note:
            clean_launch_sites_note = re.sub(
                r'<strong>note:</strong>\s*', '', launch_sites_note, flags=re.IGNORECASE)
            result["space_launch_sites_note"] = parse_text_to_list(
                clean_launch_sites_note)

    # Handle 'Space program overview'
    program_overview_data = space_data.get("Space program overview", {})
    if program_overview_data:
        # Handle 'text'
        overview_text = program_overview_data.get("text", "")
        if overview_text:
            result["space_program_overview"] = parse_text_to_list(
                overview_text)

        # Handle 'note'
        overview_note = program_overview_data.get("note", "")
        if overview_note:
            clean_overview_note = re.sub(
                r'<strong>note:</strong>\s*', '', overview_note, flags=re.IGNORECASE)
            result["space_program_overview_note"] = clean_text(
                clean_overview_note)

    return result


# Example usage
if __name__ == "__main__":
    # --------------------------------------------------------------------------------------------------
    # NOTE: "Space agency/agencies"
    # >>> ['space_agencies', 'space_agencies_note']
    # --------------------------------------------------------------------------------------------------
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # NOTE: "Space launch site(s)"
    # >>> ['space_launch_sites', 'space_launch_sites_note']
    # --------------------------------------------------------------------------------------------------
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # NOTE: "Space program overview"
    # >>> ['space_program_overview', 'space_program_overview_note']
    # --------------------------------------------------------------------------------------------------
    space_data = {
        "Space agency/agencies": {
            "text": "National Center for Space Studies (Centre National D'&eacute;tudes Spatiales, CNES; established 1961); established a military Space Command (Le Commandement de l&rsquo;Espace, CDE) under the Air and Space Force, 2020 (2024)",
            "note": ""
        },
        "Space launch site(s)": {
            "text": "Guiana Space Center (Kourou, French Guiana; also serves as the spaceport for the ESA); note &ndash; prior to the completion of the Guiana Space Center in 1969, France launched rockets from Algeria (2024)",
            "note": ""
        },
        "Space program overview": {
            "text": "has one of Europe’s largest space programs and is a key member of the European Space Agency (ESA), as well as one of its largest contributors; has independent capabilities in all areas of space categories except for autonomous manned space flight; can build, launch, and operate a range of space/satellite launch vehicles (SLVs) and spacecraft, including exploratory probes and a full spectrum of satellites; trained astronauts until training mission shifted to ESA in 2001; develops a wide range of space-related technologies; hosts the ESA headquarters; participates in international space programs such as the Square Kilometer Array Project (world’s largest radio telescope) and International Space Station (ISS); cooperates with a broad range of space agencies and commercial space companies, including those of China, Egypt, individual ESA and EU member countries, India, Indonesia, Israel, Japan, Mexico, Russia, the UAE, the US, and several African countries; has a large commercial space sector involved in such areas as satellite construction and payloads, launch capabilities, and a range of other space-related capabilities and technologies (2024)",
            "note": "<strong>note:</strong> further details about the key activities, programs, and milestones of the country’s space program, as well as government spending estimates on the space sector, appear in the Space Programs reference guide"
        }
    }
    parsed_data = parse_space(space_data)
    print(parsed_data)
