"""
Parse World-level communications data from CIA World Factbook.
Extracts global internet usage statistics by country.
"""
import re
import logging
from typing import Dict, Any, List
from bs4 import BeautifulSoup
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_communications_world(iso3Code: str, return_original: bool = False)-> dict:
    """
    Parse World-level communications data for a given country.

    Returns:
        Dict with:
            - top_internet_users: list of {country, users_millions}
            - internet_users_year: int
            - largest_data_centers: list of {name, location, area_sq_m}
    """
    result = {}
    try:
        raw_data = load_country_data(iso3Code)
    except Exception as e:
        logger.error(f"Failed to load data for {iso3Code}: {e}")
        return result

    comm_data = raw_data.get('Communications', {})
    if not comm_data or not isinstance(comm_data, dict):
        return result

    try:
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

    except Exception as e:
        logger.error(f"Error parsing communications_world for {iso3Code}: {e}")

    return result

if __name__ == "__main__":
    print("="*60)
    print("Testing parse_communications_world")
    print("="*60)
    for iso3 in ['WLD']:
        print(f"\n{iso3}:")
        try:
            result = parse_communications_world(iso3)
            if result:
                if 'top_internet_users' in result:
                    print(f"  Top internet users ({result.get('internet_users_year', 'N/A')}):")
                    for user in result['top_internet_users'][:5]:
                        print(f"    {user['country']}: {user['users_millions']} million")
                if 'largest_data_centers' in result:
                    print(f"  Largest data centers:")
                    for dc in result['largest_data_centers'][:3]:
                        print(f"    {dc['rank']}. {dc['name']} - {dc['location']}: {dc['area_sq_m']:,} sq m")
            else:
                print("  No data found")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
