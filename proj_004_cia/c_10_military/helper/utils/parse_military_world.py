"""
Parse World-level military data from CIA World Factbook.
Extracts global military personnel, deployments, arms trade.
"""
import re
import logging
from typing import Dict, Any, List

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_military_world(mil_data: dict, iso3Code: str = None) -> dict:
    """
    Parse World-level military data with detailed value extraction.

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

    return result


# Example usage
if __name__ == "__main__":
    import json
    import os

    json_path = os.path.join(os.path.dirname(__file__), '../../../../_raw_data/world/xx.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mil_data = data.get("Military and Security", {})
    parsed = parse_military_world(mil_data, "WLD")
    from pprint import pprint
    pprint(parsed)
