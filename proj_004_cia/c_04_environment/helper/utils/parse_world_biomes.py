import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')


def parse_world_biomes(biomes_data: dict, iso3Code: str = None) -> dict:
    """Parse world biomes data (primarily for World entity)."""
    result = {
        "world_biomes": {
            "types_description": None,
            "tundra": None,
            "coniferous_forest": None,
            "temperate_deciduous_forest": None,
            "rainforest": None,
            "grassland": None,
            "shrubland": None,
            "desert": None
        },
        "world_biomes_note": ""
    }

    if not biomes_data or not isinstance(biomes_data, dict):
        return result

    biome_mapping = {
        'Types of Biomes': 'types_description',
        'Tundra biome': 'tundra',
        'Coniferous Forest biome': 'coniferous_forest',
        'Temperate Deciduous Forest biome': 'temperate_deciduous_forest',
        'Rainforest biome': 'rainforest',
        'Grassland biome': 'grassland',
        'Shrubland biome': 'shrubland',
        'Desert biome': 'desert'
    }

    for field_name, result_key in biome_mapping.items():
        data = biomes_data.get(field_name, {})
        if data and isinstance(data, dict):
            text = data.get('text', '')
            if text and text.upper() != 'NA':
                result['world_biomes'][result_key] = clean_text(text)

    return result


if __name__ == "__main__":
    test_data = {
        "Types of Biomes": {"text": "A biome is a biogeographical designation..."},
        "Desert biome": {"text": "The most important characteristic of a desert..."}
    }
    print(parse_world_biomes(test_data))
