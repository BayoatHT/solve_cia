"""
Parse World-level communications data from CIA World Factbook.
Extracts global internet usage statistics by country.
"""
import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_communications_world(comm_data: dict, iso3Code: str = None) -> dict:
    """
    Parse World-level communications data with detailed value extraction.

    Returns:
        Dict with:
            - top_internet_users: list of {country, users_millions}
            - internet_users_year: int
            - largest_data_centers: list of {name, location, area_sq_m}
    """
    result = {}

    # Parse "Internet users" note
    internet_data = comm_data.get("Internet users", {})
    if internet_data:
        note = internet_data.get("note", "")
        if note:
            soup = BeautifulSoup(note, "html.parser")
            clean_text = soup.get_text()

            # Extract top countries by internet usage
            users = []
            # Pattern: "854 China; 560 India; 293 United States"
            for match in re.finditer(r'(\d+)\s+([A-Za-z\s]+?)(?:;|\(|$)', clean_text):
                users_millions = int(match.group(1))
                country = match.group(2).strip()
                if country:
                    users.append({
                        'country': country,
                        'users_millions': users_millions
                    })

            if users:
                result['top_internet_users'] = users

            # Extract year
            year_match = re.search(r'\((\d{4})\)', clean_text)
            if year_match:
                result['internet_users_year'] = int(year_match.group(1))

    # Parse "Communications - note" for data centers
    comm_note = comm_data.get("Communications - note", {})
    if comm_note:
        text = comm_note.get("text", "")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            clean_text = soup.get_text()

            # Extract data centers
            data_centers = []

            # Pattern for data center entries
            dc_matches = re.finditer(
                r'(\d+)\.\s+the\s+([^,]+?)\s+data\s+center\s+located\s+(?:in\s+)?(?:the\s+)?([^,]+),\s*([^,]+),\s*(?:China,?\s*)?(?:reportedly\s+)?covers\s+([\d,.]+)\s*(million\s+)?sq\s*m',
                clean_text, re.IGNORECASE
            )
            for match in dc_matches:
                rank = int(match.group(1))
                name = match.group(2).strip()
                location = f"{match.group(3).strip()}, {match.group(4).strip()}"
                area = float(match.group(5).replace(',', ''))
                if match.group(6):  # million
                    area *= 1_000_000

                data_centers.append({
                    'rank': rank,
                    'name': name,
                    'location': location,
                    'area_sq_m': int(area)
                })

            if data_centers:
                result['largest_data_centers'] = data_centers

    return result


# Example usage
if __name__ == "__main__":
    import json
    import os

    json_path = os.path.join(os.path.dirname(__file__), '../../../../_raw_data/world/xx.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    comm_data = data.get("Communications", {})
    parsed = parse_communications_world(comm_data, "WLD")
    from pprint import pprint
    pprint(parsed)
