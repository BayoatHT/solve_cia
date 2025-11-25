"""Extract national_symbol for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_national_symbol(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse national_symbol from raw data."""
    gov_section = raw_data.get('Government', {})
    field_data = gov_section.get('National symbol(s)', {})

    return {
        'national_symbol': field_data.get('text', '').strip() if isinstance(field_data, dict) else ''
    }


def extract_national_symbol(parsed_data: Dict) -> str:
    """Extract national_symbol from parsed data."""
    return parsed_data.get('national_symbol', '')


def get_national_symbol(verbose: bool = False) -> Dict[str, str]:
    """
    Get national_symbol for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to national_symbol values

    Example:
        >>> data = get_national_symbol()
        >>> data['USA']
        'bald eagle; national colors: red, white, blue'
    """
    return extract_string_feature(
        parse_national_symbol,
        extract_national_symbol,
        'national_symbol',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_national_symbol(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
