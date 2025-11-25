"""Extract legal_system for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_legal_system(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse legal_system from raw data."""
    section = raw_data.get('Government', {})
    field_data = section.get('Legal system', {})

    return {
        'legal_system': field_data.get('text', '').strip() if isinstance(field_data, dict) else ''
    }


def extract_legal_system(parsed_data: Dict) -> str:
    """Extract legal_system from parsed data."""
    return parsed_data.get('legal_system', '')


def get_legal_system(verbose: bool = False) -> Dict[str, str]:
    """
    Get legal_system for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to legal_system values

    Example:
        >>> data = get_legal_system()
        >>> data['USA']
        'common law system based on English common law'
    """
    return extract_string_feature(
        parse_legal_system,
        extract_legal_system,
        'legal_system',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_legal_system(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:60]}..." if len(val) > 60 else val
        print(f"  {iso3}: {display}")
