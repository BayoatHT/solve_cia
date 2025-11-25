import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.parse_text_to_list import parse_text_to_list
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_space(iso3Code: str) -> dict:
    """
    Parse space program data from CIA Space section for a given country.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A dictionary containing parsed information for space agencies, launch sites, and overview.
    """
    result = {
        "space_agencies": [],
        "space_agencies_note": "",
        "space_launch_sites": [],
        "space_launch_sites_note": [],
        "space_program_overview": [],
        "space_program_overview_note": ""
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    space_data = raw_data.get('Space', {})

    if not space_data or not isinstance(space_data, dict):
        return result

    try:
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
                result["space_launch_sites"] = parse_text_to_list(launch_sites_text)

            # Handle 'note'
            launch_sites_note = launch_sites_data.get("note", "")
            if launch_sites_note:
                clean_launch_sites_note = re.sub(
                    r'<strong>note:</strong>\s*', '', launch_sites_note, flags=re.IGNORECASE)
                result["space_launch_sites_note"] = parse_text_to_list(clean_launch_sites_note)

        # Handle 'Space program overview'
        program_overview_data = space_data.get("Space program overview", {})
        if program_overview_data:
            # Handle 'text'
            overview_text = program_overview_data.get("text", "")
            if overview_text:
                result["space_program_overview"] = parse_text_to_list(overview_text)

            # Handle 'note'
            overview_note = program_overview_data.get("note", "")
            if overview_note:
                clean_overview_note = re.sub(
                    r'<strong>note:</strong>\s*', '', overview_note, flags=re.IGNORECASE)
                result["space_program_overview_note"] = clean_text(clean_overview_note)

    except Exception as e:
        logger.error(f"Error parsing space for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_space")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'IND', 'FRA', 'JPN']:
        print(f"\n{iso3}:")
        try:
            result = parse_space(iso3)
            if result.get('space_agencies'):
                agencies = result['space_agencies']
                print(f"  Agencies: {len(agencies)}")
                if agencies:
                    print(f"    First: {str(agencies[0])[:50]}...")
            if result.get('space_launch_sites'):
                print(f"  Launch sites: {len(result['space_launch_sites'])}")
            if not result.get('space_agencies') and not result.get('space_launch_sites'):
                print("  No space data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
