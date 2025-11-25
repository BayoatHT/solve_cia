"""Extract internet country code for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_internet_country_code(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse internet country code from raw data."""
    comms_section = raw_data.get('Communications', {})
    code_data = comms_section.get('Internet country code', {})

    return {
        'internet_country_code': code_data.get('text', '').strip() if isinstance(code_data, dict) else ''
    }


def extract_internet_country_code(parsed_data: Dict) -> str:
    """Extract internet country code from parsed data."""
    return parsed_data.get('internet_country_code', '')


def get_internet_country_code(verbose: bool = False) -> Dict[str, str]:
    """
    Get internet country code for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to internet country codes

    Example:
        >>> codes = get_internet_country_code()
        >>> codes['USA']
        '.us'
        >>> codes['FRA']
        '.fr'
    """
    return extract_string_feature(
        parse_internet_country_code,
        extract_internet_country_code,
        'internet_country_code',
        verbose=verbose
    )


if __name__ == "__main__":
    codes = get_internet_country_code(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'JPN', 'GBR']:
        print(f"  {iso3}: {codes.get(iso3, 'N/A')}")
