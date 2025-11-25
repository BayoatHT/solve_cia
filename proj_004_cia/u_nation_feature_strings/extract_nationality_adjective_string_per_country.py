"""Extract nationality_adjective for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_nationality_adjective(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse nationality_adjective from raw data."""
    section = raw_data.get('People and Society', {})
    field_data = section.get('Nationality', {})
    
    value = ''
    if isinstance(field_data, dict):
        subfield = field_data.get('adjective', {})
        if isinstance(subfield, dict):
            value = subfield.get('text', '').strip()

    return {'nationality_adjective': value}


def extract_nationality_adjective(parsed_data: Dict) -> str:
    """Extract nationality_adjective from parsed data."""
    return parsed_data.get('nationality_adjective', '')


def get_nationality_adjective(verbose: bool = False) -> Dict[str, str]:
    """
    Get nationality_adjective for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to nationality_adjective values

    Example:
        >>> data = get_nationality_adjective()
        >>> data['USA']
        'American'
    """
    return extract_string_feature(
        parse_nationality_adjective,
        extract_nationality_adjective,
        'nationality_adjective',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_nationality_adjective(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'GBR']:
        val = data.get(iso3, 'N/A')
        print(f"  {iso3}: {val}")
