"""Extract terrain description for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_terrain(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse terrain from raw data."""
    geo_section = raw_data.get('Geography', {})
    terrain_data = geo_section.get('Terrain', {})

    return {
        'terrain': terrain_data.get('text', '').strip() if isinstance(terrain_data, dict) else ''
    }


def extract_terrain(parsed_data: Dict) -> str:
    """Extract terrain from parsed data."""
    return parsed_data.get('terrain', '')


def get_terrain(verbose: bool = False) -> Dict[str, str]:
    """
    Get terrain for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to terrain values

    Example:
        >>> data = get_terrain()
        >>> data['USA']
        'vast central plain, mountains in west, hills and low mountains in east'
    """
    return extract_string_feature(
        parse_terrain,
        extract_terrain,
        'terrain',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_terrain(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
