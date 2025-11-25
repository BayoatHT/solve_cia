import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_military_forces(iso3Code: str) -> dict:
    """
    Parse military forces data from CIA Military and Security section for a given country.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (e.g., 'USA', 'CHN')

    Returns:
        dict: A structured dictionary containing branches, abbreviations, metadata, and notes.
    """
    result = {
        "branches": [],
        "year": "",
        "military_note": []
    }

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    military_section = raw_data.get('Military and Security', {})
    military_forces_data = military_section.get('Military and security forces', {})

    if not military_forces_data or not isinstance(military_forces_data, dict):
        return result

    try:
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

    except Exception as e:
        logger.error(f"Error parsing military forces for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_forces")
    print("=" * 60)
    for iso3 in ['USA', 'CHN', 'RUS', 'DEU', 'GBR', 'FRA']:
        print(f"\n{iso3}:")
        try:
            result = parse_military_forces(iso3)
            if result.get('branches'):
                print(f"  Branches: {len(result['branches'])}")
                for b in result['branches'][:2]:
                    branch = b.get('branch', '')[:60]
                    print(f"    - {branch}...")
            if result.get('year'):
                print(f"  Year: {result['year']}")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
