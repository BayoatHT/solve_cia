
######################################################################################################################
#   CORE IMPORTS
# ---------------------------------------------------------------------------------------------------------------------
import os
import re
import logging
from bs4 import BeautifulSoup
from proj_004_cia.c_00_transform_utils.clean_text import clean_text
from proj_004_cia.c_00_transform_utils.extract_numeric_value import extract_numeric_value
# ------------------------------------------------------------------------------------------------------------------


def parse_terrain(terrain_data: dict, iso3Code: str = None) -> list:
    """
    Parses the 'Terrain' data.

    Parameters:
        terrain_data (dict): The 'Terrain' section from the data.
        iso3Code (str): The ISO3 code of the country.

    Returns:
        list: A list of dictionaries containing terrain details for each region or the country as a whole.
    """
    result = []

    terrain_text = terrain_data.get('text', '')
    if terrain_text:
        # Use BeautifulSoup to parse HTML and extract region descriptions
        soup = BeautifulSoup(terrain_text, 'html.parser')
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            strong_tag = p.find('strong')
            if strong_tag:
                region = strong_tag.get_text(strip=True).rstrip(':')
                description = p.get_text(strip=True).replace(
                    strong_tag.get_text(strip=True), '').lstrip(':').strip()
                result.append({
                    'region': region,
                    'description': description
                })
            else:
                # If no specific region, use the country ISO3 code
                result.append({
                    'region': iso3Code,
                    'description': p.get_text(strip=True)
                })
    else:
        # If no terrain data is available, add a default entry with ISO3 code
        result.append({
            'region': iso3Code,
            'description': ''
        })

    return result
