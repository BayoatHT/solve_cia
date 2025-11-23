"""
Parse World-level transportation data from CIA World Factbook.
Extracts global airports, heliports, waterways statistics.
"""
import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_transportation_world(trans_data: dict, iso3Code: str = None) -> dict:
    """
    Parse World-level transportation data with detailed value extraction.

    Returns:
        Dict with:
            - airports_worldwide_value: int
            - airports_year: int
            - heliports_worldwide_value: int
            - heliports_year: int
            - top_rivers_navigable: list of {name, location, length_km}
            - top_lakes_navigable: list of {name, location, area_sq_km}
            - countries_without_rivers_count: int
    """
    result = {}

    # Parse "Airports"
    airports_data = trans_data.get("Airports", {})
    if airports_data:
        text = airports_data.get("text", "")
        if text:
            match = re.search(r'([\d,]+)\s*\((\d{4})\)', text)
            if match:
                result['airports_worldwide_value'] = int(match.group(1).replace(',', ''))
                result['airports_year'] = int(match.group(2))

    # Parse "Heliports"
    heliports_data = trans_data.get("Heliports", {})
    if heliports_data:
        text = heliports_data.get("text", "")
        if text:
            match = re.search(r'([\d,]+)\s*\((\d{4})\)', text)
            if match:
                result['heliports_worldwide_value'] = int(match.group(1).replace(',', ''))
                result['heliports_year'] = int(match.group(2))

    # Parse "Waterways" note for rivers/lakes
    waterways_data = trans_data.get("Waterways", {})
    if waterways_data:
        note = waterways_data.get("note", "")
        if note:
            soup = BeautifulSoup(note, "html.parser")
            clean_text = soup.get_text()

            # Extract top rivers
            rivers = []
            rivers_match = re.search(r'top ten longest rivers[:\s]*(.+?)(?=note|top ten largest|$)', clean_text, re.IGNORECASE | re.DOTALL)
            if rivers_match:
                for match in re.finditer(r'([A-Za-z\-/\s]+)\s*\(([^)]+)\)\s*([\d,]+)\s*km', rivers_match.group(1)):
                    rivers.append({
                        'name': match.group(1).strip(),
                        'location': match.group(2).strip(),
                        'length_km': int(match.group(3).replace(',', ''))
                    })
            if rivers:
                result['top_rivers_navigable'] = rivers

            # Extract top lakes
            lakes = []
            lakes_match = re.search(r'top ten largest natural lakes[:\s]*(.+?)(?=note|$)', clean_text, re.IGNORECASE | re.DOTALL)
            if lakes_match:
                for match in re.finditer(r'([A-Za-z\s]+)\s*\(([^)]+)\)\s*([\d,]+)\s*sq\s*km', lakes_match.group(1)):
                    lakes.append({
                        'name': match.group(1).strip(),
                        'location': match.group(2).strip(),
                        'area_sq_km': int(match.group(3).replace(',', ''))
                    })
            if lakes:
                result['top_lakes_navigable'] = lakes

            # Countries without rivers
            no_rivers_match = re.search(r'(\d+)\s+countries\s+without\s+rivers', clean_text, re.IGNORECASE)
            if no_rivers_match:
                result['countries_without_rivers_count'] = int(no_rivers_match.group(1))

    return result


# Example usage
if __name__ == "__main__":
    import json
    import os

    json_path = os.path.join(os.path.dirname(__file__), '../../../../_raw_data/world/xx.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    trans_data = data.get("Transportation", {})
    parsed = parse_transportation_world(trans_data, "WLD")
    from pprint import pprint
    pprint(parsed)
