"""Extract independence for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_independence(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse independence from raw data."""
    gov_section = raw_data.get('Government', {})
    field_data = gov_section.get('Independence', {})

    return {
        'independence': field_data.get('text', '').strip() if isinstance(field_data, dict) else ''
    }


def extract_independence(parsed_data: Dict) -> str:
    """Extract independence from parsed data."""
    return parsed_data.get('independence', '')


def get_independence(verbose: bool = False) -> Dict[str, str]:
    """
    Get independence for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to independence values

    Example:
        >>> data = get_independence()
        >>> data['USA']
        '4 July 1776 (declared independence from Great Britain)'
    """
    return extract_string_feature(
        parse_independence,
        extract_independence,
        'independence',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_independence(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
