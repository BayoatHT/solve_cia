import re
import logging
from proj_004_cia.c_00_transform_utils.clean_text import clean_text

logging.basicConfig(level='WARNING', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def parse_world_biomes(biomes_data: dict, iso3Code: str = None, return_original: bool = False) -> dict:
    """
    Parse world biomes from CIA Environment section (primarily for World entity).

    Args:
        biomes_data: The 'World biomes' section data
        iso3Code: ISO3 country code for logging purposes
        return_original: If True, return raw data without parsing

    Returns:
        Dictionary with structured world biomes data
    """
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

    if return_original:
        return biomes_data

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
    from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data

    print("="*60)
    print("Testing parse_world_biomes")
    print("="*60)
    # World biomes only exists for World entity
    for iso3 in ['WLD', 'USA', 'CHN']:
        print(f"\n{iso3}:")
        try:
            raw_data = load_country_data(iso3)
            biomes_data = raw_data.get('Environment', {}).get('World biomes', {})
            result = parse_world_biomes(biomes_data, iso3)
            wb = result['world_biomes']
            has_data = any(v for v in wb.values() if v)
            if has_data:
                if wb['types_description']:
                    print(f"  Types: {wb['types_description'][:60]}...")
                biomes_found = [k for k, v in wb.items() if v and k != 'types_description']
                print(f"  Biomes with data: {len(biomes_found)}")
                for biome in biomes_found[:2]:
                    print(f"    - {biome}")
            else:
                print("  No world biomes data (expected for country)")
        except Exception as e:
            print(f"  ERROR: {str(e)[:60]}")
    print("\n" + "="*60)
    print("✓ Tests complete")
