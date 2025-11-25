"""Extract map reference for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_map_reference(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse map reference from raw data."""
    geo_section = raw_data.get('Geography', {})
    map_ref_data = geo_section.get('Map references', {})

    return {
        'map_references': map_ref_data.get('text', '').strip() if isinstance(map_ref_data, dict) else ''
    }


def extract_map_reference(parsed_data: Dict) -> str:
    """Extract map reference from parsed data."""
    return parsed_data.get('map_references', '')


def get_map_reference(verbose: bool = False) -> Dict[str, str]:
    """
    Get map reference for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to map reference values

    Example:
        >>> data = get_map_reference()
        >>> data['USA']
        'North America'
    """
    return extract_string_feature(
        parse_map_reference,
        extract_map_reference,
        'map_references',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_map_reference(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
