"""Extract government type for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_government_type(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse government type from raw data."""
    gov_section = raw_data.get('Government', {})
    gov_type = gov_section.get('Government type', {})

    return {
        'government_type': gov_type.get('text', '').strip() if isinstance(gov_type, dict) else ''
    }


def extract_government_type(parsed_data: Dict) -> str:
    """Extract government type from parsed data."""
    return parsed_data.get('government_type', '')


def get_government_type(verbose: bool = False) -> Dict[str, str]:
    """
    Get government type for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to government types

    Example:
        >>> gov_types = get_government_type()
        >>> gov_types['USA']
        'constitutional federal republic'
        >>> gov_types['GBR']
        'parliamentary constitutional monarchy'
    """
    return extract_string_feature(
        parse_government_type,
        extract_government_type,
        'government_type',
        verbose=verbose
    )


if __name__ == "__main__":
    gov_types = get_government_type(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'GBR', 'SAU']:
        print(f"  {iso3}: {gov_types.get(iso3, 'N/A')}")
