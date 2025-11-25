"""
Parse World-level military data from CIA World Factbook.
Extracts global military personnel, deployments, arms trade.
"""
import re
import logging
from typing import Dict, Any, List
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_military_world(iso3Code: str = 'WLD', return_original: bool = False)-> dict:
    """
    Parse World-level military data with detailed value extraction.

    Args:
        iso3Code: ISO 3166-1 alpha-3 country code (default: 'WLD' for World)

    Returns:
        Dict with:
            - military_personnel_worldwide_value: int
            - military_personnel_year: int
            - largest_militaries: list of country names
            - un_peacekeeping_personnel_value: int
            - un_peacekeeping_year: int
            - leading_arms_exporter: str
            - leading_arms_exporter_year: int
    """
    result = {}

    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    mil_data = raw_data.get('Military and Security', {})

    if not mil_data or not isinstance(mil_data, dict):
        return result

    try:
        # Parse "Military and security service personnel strengths"
        personnel_data = mil_data.get("Military and security service personnel strengths", {})
        if personnel_data:
            text = personnel_data.get("text", "")
            note = personnel_data.get("note", "")

            if text:
                # Match "approximately 20 million active-duty military personnel worldwide (2023)"
                match = re.search(r'(?:approximately\s+)?([\d.]+)\s*(million)', text, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    result['military_personnel_worldwide_value'] = int(value * 1_000_000)

                year_match = re.search(r'\((\d{4})\)', text)
                if year_match:
                    result['military_personnel_year'] = int(year_match.group(1))

            if note:
                # Extract largest militaries
                countries_match = re.search(r'largest militaries.*?belong to\s+(.+)', note, re.IGNORECASE)
                if countries_match:
                    countries_str = countries_match.group(1)
                    # Clean and split
                    countries_str = re.sub(r'and\s+', ', ', countries_str)
                    countries = [c.strip() for c in countries_str.split(',') if c.strip()]
                    if countries:
                        result['largest_militaries'] = countries

        # Parse "Military deployments"
        deploy_data = mil_data.get("Military deployments", {})
        if deploy_data:
            text = deploy_data.get("text", "")
            if text:
                # Match "approximately 65,000 personnel deployed on UN peacekeeping missions"
                match = re.search(r'(?:approximately\s+)?([\d,]+)\s+personnel\s+deployed', text, re.IGNORECASE)
                if match:
                    result['un_peacekeeping_personnel_value'] = int(match.group(1).replace(',', ''))

                year_match = re.search(r'\((\d{4})\)', text)
                if year_match:
                    result['un_peacekeeping_year'] = int(year_match.group(1))

        # Parse "Military equipment inventories and acquisitions"
        equip_data = mil_data.get("Military equipment inventories and acquisitions", {})
        if equip_data:
            text = equip_data.get("text", "")
            if text:
                # Match "the US is the world's leading arms exporter (2023)"
                match = re.search(r'the\s+(\w+)\s+is\s+the\s+world\'?s?\s+leading\s+arms\s+exporter', text, re.IGNORECASE)
                if match:
                    result['leading_arms_exporter'] = match.group(1)

                year_match = re.search(r'\((\d{4})\)', text)
                if year_match:
                    result['leading_arms_exporter_year'] = int(year_match.group(1))

    except Exception as e:
        logger.error(f"Error parsing military world for {iso3Code}: {e}")

    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing parse_military_world")
    print("=" * 60)
    print("\nWLD:")
    try:
        result = parse_military_world('WLD')
        if result:
            if result.get('military_personnel_worldwide_value'):
                print(f"  Global personnel: {result['military_personnel_worldwide_value']:,}")
            if result.get('largest_militaries'):
                print(f"  Largest militaries: {', '.join(result['largest_militaries'][:5])}")
            if result.get('un_peacekeeping_personnel_value'):
                print(f"  UN peacekeeping: {result['un_peacekeeping_personnel_value']:,}")
            if result.get('leading_arms_exporter'):
                print(f"  Leading exporter: {result['leading_arms_exporter']}")
        else:
            print("  No world data found")
    except Exception as e:
        print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "=" * 60)
    print("✓ Tests complete")
