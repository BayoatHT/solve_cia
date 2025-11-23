"""
Parse World-level geography data from CIA World Factbook.
Extracts global rankings: largest entities, lakes, rivers, islands, mountains, etc.
"""
import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_ranking_list(text: str, pattern: str) -> List[Dict[str, Any]]:
    """
    Parse a ranking list like 'Name (location) 1,234 sq km' into structured data.
    """
    results = []
    # Pattern to match: Name (location) number unit
    item_pattern = re.compile(
        r'([^;]+?)\s*(?:\(([^)]+)\))?\s*([\d,]+(?:\.\d+)?)\s*(sq km|km)',
        re.IGNORECASE
    )

    for match in item_pattern.finditer(text):
        name = match.group(1).strip()
        location = match.group(2).strip() if match.group(2) else None
        value = float(match.group(3).replace(',', ''))
        unit = match.group(4)

        item = {
            'name': name,
            'value': int(value) if value == int(value) else value,
            'unit': unit
        }
        if location:
            item['location'] = location
        results.append(item)

    return results


def parse_geography_world(geo_data: dict, iso3Code: str = None) -> dict:
    """
    Parse World-level geography data with detailed value extraction.

    Returns:
        Dict with:
            - top_entities_by_area: list of {name, value, unit}
            - top_water_bodies: list of {name, value, unit}
            - top_landmasses: list of {name, value, unit}
            - top_islands: list of {name, location, value, unit}
            - top_lakes: list of {name, location, value, unit}
            - top_rivers: list of {name, location, value, unit}
            - irrigated_land_total_sq_km: int
            - countries_without_rivers: list
    """
    result = {}

    # Parse "Area - rankings"
    area_rankings = geo_data.get("Area - rankings", {})
    if area_rankings:
        text = area_rankings.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Top entities by size
            entities_match = re.search(
                r'top fifteen.*?ranked by size[:\s]*(.+?)(?=top ten largest water|$)',
                clean_text, re.IGNORECASE | re.DOTALL
            )
            if entities_match:
                entities = []
                for match in re.finditer(r'([A-Za-z\s]+)\s+([\d,]+)\s*sq\s*km', entities_match.group(1)):
                    entities.append({
                        'name': match.group(1).strip(),
                        'area_sq_km': int(match.group(2).replace(',', ''))
                    })
                if entities:
                    result['top_entities_by_area'] = entities

            # Top water bodies
            water_match = re.search(
                r'top ten largest water bodies[:\s]*(.+?)(?=top ten largest landmasses|$)',
                clean_text, re.IGNORECASE | re.DOTALL
            )
            if water_match:
                water_bodies = []
                for match in re.finditer(r'([A-Za-z\s]+)\s+([\d,]+)\s*sq\s*km', water_match.group(1)):
                    water_bodies.append({
                        'name': match.group(1).strip(),
                        'area_sq_km': int(match.group(2).replace(',', ''))
                    })
                if water_bodies:
                    result['top_water_bodies'] = water_bodies

            # Top landmasses
            land_match = re.search(
                r'top ten largest landmasses[:\s]*(.+?)(?=top ten largest islands|$)',
                clean_text, re.IGNORECASE | re.DOTALL
            )
            if land_match:
                landmasses = []
                for match in re.finditer(r'([A-Za-z\s]+)\s+([\d,]+)\s*sq\s*km', land_match.group(1)):
                    landmasses.append({
                        'name': match.group(1).strip(),
                        'area_sq_km': int(match.group(2).replace(',', ''))
                    })
                if landmasses:
                    result['top_landmasses'] = landmasses

            # Top islands
            islands_match = re.search(
                r'top ten largest islands[:\s]*(.+?)(?=top ten longest mountain|$)',
                clean_text, re.IGNORECASE | re.DOTALL
            )
            if islands_match:
                islands = []
                for match in re.finditer(r'([A-Za-z\s]+)\s*\(([^)]+)\)\s*([\d,]+)\s*sq\s*km', islands_match.group(1)):
                    islands.append({
                        'name': match.group(1).strip(),
                        'location': match.group(2).strip(),
                        'area_sq_km': int(match.group(3).replace(',', ''))
                    })
                if islands:
                    result['top_islands'] = islands

    # Parse "Major lakes"
    lakes_data = geo_data.get("Major lakes (area sq km)", {})
    if lakes_data:
        text = lakes_data.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            lakes = []
            for match in re.finditer(r'([A-Za-z\s]+)\s*\(([^)]+)\)\s*([\d,]+)\s*sq\s*km', clean_text):
                lakes.append({
                    'name': match.group(1).strip(),
                    'location': match.group(2).strip(),
                    'area_sq_km': int(match.group(3).replace(',', ''))
                })
            if lakes:
                result['top_lakes'] = lakes

    # Parse "Major rivers"
    rivers_data = geo_data.get("Major rivers (by length in km)", {})
    if rivers_data:
        text = rivers_data.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            rivers = []
            for match in re.finditer(r'([A-Za-z\-/\s]+)\s*\(([^)]+)\)\s*([\d,]+)\s*km', clean_text):
                rivers.append({
                    'name': match.group(1).strip(),
                    'location': match.group(2).strip(),
                    'length_km': int(match.group(3).replace(',', ''))
                })
            if rivers:
                result['top_rivers'] = rivers

            # Countries without rivers
            no_rivers_match = re.search(r'(\d+)\s+countries\s+without\s+rivers', clean_text, re.IGNORECASE)
            if no_rivers_match:
                result['countries_without_rivers_count'] = int(no_rivers_match.group(1))

    # Parse "Irrigated land"
    irrigated_data = geo_data.get("Irrigated land", {})
    if irrigated_data:
        text = irrigated_data.get("text", "")
        if text:
            match = re.search(r'([\d,.]+)\s*(million)?\s*sq\s*km', text, re.IGNORECASE)
            if match:
                value = float(match.group(1).replace(',', ''))
                if match.group(2):
                    value *= 1_000_000
                result['irrigated_land_total_sq_km'] = int(value)

    # Parse "Land boundaries"
    boundaries_data = geo_data.get("Land boundaries", {})
    if boundaries_data:
        text = boundaries_data.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Total land boundaries
            total_match = re.search(r'total[:\s]*([\d,]+)\s*km', clean_text, re.IGNORECASE)
            if total_match:
                result['land_boundaries_total_km'] = int(total_match.group(1).replace(',', ''))

            # Count of international land boundaries
            count_match = re.search(r'(\d+)\s+international\s+land\s+boundaries', clean_text, re.IGNORECASE)
            if count_match:
                result['international_boundaries_count'] = int(count_match.group(1))

    return result


# Example usage
if __name__ == "__main__":
    import json
    import os

    # Test with World data
    json_path = os.path.join(os.path.dirname(__file__), '../../../../_raw_data/world/xx.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    geo_data = data.get("Geography", {})
    parsed = parse_geography_world(geo_data, "WLD")
    from pprint import pprint
    pprint(parsed)
