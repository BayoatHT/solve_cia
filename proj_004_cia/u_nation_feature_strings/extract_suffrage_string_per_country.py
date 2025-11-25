"""Extract suffrage for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_suffrage(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse suffrage from raw data."""
    gov_section = raw_data.get('Government', {})
    field_data = gov_section.get('Suffrage', {})

    return {
        'suffrage': field_data.get('text', '').strip() if isinstance(field_data, dict) else ''
    }


def extract_suffrage(parsed_data: Dict) -> str:
    """Extract suffrage from parsed data."""
    return parsed_data.get('suffrage', '')


def get_suffrage(verbose: bool = False) -> Dict[str, str]:
    """
    Get suffrage for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to suffrage values

    Example:
        >>> data = get_suffrage()
        >>> data['USA']
        '18 years of age; universal'
    """
    return extract_string_feature(
        parse_suffrage,
        extract_suffrage,
        'suffrage',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_suffrage(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
