"""Extract climate for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_climate(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse climate from raw data."""
    section = raw_data.get('Geography', {})
    field_data = section.get('Climate', {})

    return {
        'climate': field_data.get('text', '').strip() if isinstance(field_data, dict) else ''
    }


def extract_climate(parsed_data: Dict) -> str:
    """Extract climate from parsed data."""
    return parsed_data.get('climate', '')


def get_climate(verbose: bool = False) -> Dict[str, str]:
    """
    Get climate for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to climate values

    Example:
        >>> data = get_climate()
        >>> data['USA']
        'mostly temperate, but tropical in Hawaii and Florida'
    """
    return extract_string_feature(
        parse_climate,
        extract_climate,
        'climate',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_climate(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:60]}..." if len(val) > 60 else val
        print(f"  {iso3}: {display}")
