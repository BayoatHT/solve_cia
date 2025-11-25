"""
Parse World-level space data from CIA World Factbook.
Extracts global space statistics including agency counts, launch sites, satellite counts.
"""
import re
import logging
from typing import Dict, Any
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_space_world(iso3Code: str = 'WLD', return_original: bool = False)-> dict:
    """
    Parse World-level space data with detailed value extraction.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (default: 'WLD' for World)

    Returns:
        Dict with extracted values:
            - space_agencies_count: int (number of countries with space agencies)
            - space_agencies_year: int
            - launch_sites_count: int (number of countries with launch sites)
            - launch_sites_year: int
            - annual_launches_value: int (attempted launches worldwide)
            - annual_launches_year: int
            - satellites_total_value: int (total satellites in orbit)
            - satellites_active_value: int (active satellites)
            - satellites_year: int

    Example:
        Output: {'space_agencies_count': 70, 'space_agencies_year': 2024, ...}
    """
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    space_data = raw_data.get('Space', {})

    if not space_data or not isinstance(space_data, dict):
        return result

    try:
        # Parse "Space agency/agencies"
        agencies_data = space_data.get("Space agency/agencies", {})
        if agencies_data:
            text = agencies_data.get("text", "")
            if text:
                # Extract count: "more than 70 countries"
                count_match = re.search(r'(?:more than\s+)?(\d+)\s+countries', text, re.IGNORECASE)
                if count_match:
                    result["space_agencies_count"] = int(count_match.group(1))
                    result["space_agencies_is_minimum"] = "more than" in text.lower()

                # Extract year
                year_match = re.search(r'\((\d{4})\)', text)
                if year_match:
                    result["space_agencies_year"] = int(year_match.group(1))

        # Parse "Space launch site(s)"
        launch_data = space_data.get("Space launch site(s)", {})
        if launch_data:
            text = launch_data.get("text", "")
            note = launch_data.get("note", "")

            if text:
                # Extract count: "more than 30 countries"
                count_match = re.search(r'(?:more than\s+)?(\d+)\s+countries', text, re.IGNORECASE)
                if count_match:
                    result["launch_sites_count"] = int(count_match.group(1))
                    result["launch_sites_is_minimum"] = "more than" in text.lower()

                # Extract year
                year_match = re.search(r'\((\d{4})\)', text)
                if year_match:
                    result["launch_sites_year"] = int(year_match.group(1))

            if note:
                # Extract launch attempts: "approximately 220 attempted space launches worldwide in 2023"
                launches_match = re.search(r'(?:approximately\s+)?(\d+)\s+(?:attempted\s+)?space\s+launches', note, re.IGNORECASE)
                if launches_match:
                    result["annual_launches_value"] = int(launches_match.group(1))

                # Extract launch year
                launch_year_match = re.search(r'launches\s+(?:worldwide\s+)?in\s+(\d{4})', note, re.IGNORECASE)
                if launch_year_match:
                    result["annual_launches_year"] = int(launch_year_match.group(1))

                # Extract total satellites: "over 11,000 satellites in orbit"
                total_sat_match = re.search(r'(?:over\s+)?([\d,]+)\s+satellites\s+in\s+orbit', note, re.IGNORECASE)
                if total_sat_match:
                    result["satellites_total_value"] = int(total_sat_match.group(1).replace(',', ''))
                    result["satellites_total_is_minimum"] = "over" in note.lower()

                # Extract active satellites: "about 9,000 were still active"
                active_sat_match = re.search(r'(?:about\s+)?([\d,]+)\s+(?:were\s+)?(?:still\s+)?active', note, re.IGNORECASE)
                if active_sat_match:
                    result["satellites_active_value"] = int(active_sat_match.group(1).replace(',', ''))

                # Extract satellites year: "as of December 2023"
                sat_year_match = re.search(r'as\s+of\s+(?:\w+\s+)?(\d{4})', note, re.IGNORECASE)
                if sat_year_match:
                    result["satellites_year"] = int(sat_year_match.group(1))

        # Parse "Space program overview" if exists
        overview_data = space_data.get("Space program overview", {})
        if overview_data:
            text = overview_data.get("text", "")
            if text:
                result["space_program_overview"] = text

    except Exception as e:
        logger.error(f"Error parsing space world for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_space_world")
    print("=" * 60)
    print("\nWLD:")
    try:
        result = parse_space_world('WLD')
        if result:
            if result.get('space_agencies_count'):
                print(f"  Space agencies: {result['space_agencies_count']} countries")
            if result.get('launch_sites_count'):
                print(f"  Launch sites: {result['launch_sites_count']} countries")
            if result.get('satellites_total_value'):
                print(f"  Satellites in orbit: {result['satellites_total_value']:,}")
            if result.get('annual_launches_value'):
                print(f"  Annual launches: {result['annual_launches_value']}")
        else:
            print("  No world space data found")
    except Exception as e:
        print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
