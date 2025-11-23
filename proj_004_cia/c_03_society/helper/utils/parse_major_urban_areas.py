import re
import logging
from typing import Dict, List, Optional
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

# Configure logging
logging.basicConfig(level='WARNING',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_major_urban_areas(major_urban_data: dict, iso3Code: str = None) -> dict:
    """
    Parse major urban areas population from CIA World Factbook format.

    Handles format:
    "18.937 million New York-Newark, 12.534 million Los Angeles, 5.490 million WASHINGTON, D.C. (capital) (2023)"
    """
    result = {
        "major_urban_areas": [],
        "major_urban_areas_timestamp": None,
        "major_urban_areas_raw": None
    }

    if not major_urban_data or not isinstance(major_urban_data, dict):
        return result

    text = major_urban_data.get('text', '').strip()

    if not text or text.upper() == 'NA':
        return result

    result["major_urban_areas_raw"] = text

    # Extract year from end of text
    year_match = re.search(r'\((\d{4})\)\s*$', text)
    if year_match:
        result["major_urban_areas_timestamp"] = year_match.group(1)
        text = text[:year_match.start()].strip()

    # Pattern to match: "18.937 million City Name" or "35,000 CITY (capital)"
    # Split by comma, handling city names with commas carefully
    entries = []

    # Pattern: number + optional "million" + city name
    pattern = re.compile(r'([\d.,]+)\s*(million|thousand)?\s+([^,]+?)(?:,|$)')

    for match in pattern.finditer(text):
        pop_str = match.group(1).replace(',', '')
        multiplier = match.group(2)
        city_name = match.group(3).strip()

        try:
            population = float(pop_str)
            if multiplier == 'million':
                population = int(population * 1_000_000)
            elif multiplier == 'thousand':
                population = int(population * 1_000)
            else:
                population = int(population)
        except ValueError:
            continue

        # Check if capital
        is_capital = '(capital)' in city_name.lower()
        city_name = re.sub(r'\s*\(capital\)\s*', '', city_name, flags=re.IGNORECASE).strip()

        entries.append({
            "city": city_name,
            "population": population,
            "is_capital": is_capital
        })

    result["major_urban_areas"] = entries

    return result


if __name__ == "__main__":
    test1 = {
        "text": "18.937 million New York-Newark, 12.534 million Los Angeles-Long Beach-Santa Ana, 5.490 million WASHINGTON, D.C. (capital) (2023)"
    }
    print(parse_major_urban_areas(test1))
