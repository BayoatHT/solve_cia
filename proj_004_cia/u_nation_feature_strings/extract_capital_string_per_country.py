"""Extract capital city name for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.c_05_government.return_government_data import return_government_data


def extract_capital(parsed_data: Dict) -> str:
    """
    Extract capital city name from parsed government data.

    Args:
        parsed_data: Parsed government data dictionary

    Returns:
        Capital city name as string
    """
    # Try to get capital_name directly
    name = parsed_data.get('capital_name', '')
    if isinstance(name, str) and name:
        return name.strip()

    # Fallback: try capital dict with name field
    capital_data = parsed_data.get('capital', {})
    if isinstance(capital_data, dict):
        name = capital_data.get('capital_name', '')
        if isinstance(name, str) and name:
            return name.strip()

    return ''


def get_capital(verbose: bool = False) -> Dict[str, str]:
    """
    Get capital city for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to capital city names

    Example:
        >>> capitals = get_capital()
        >>> capitals['USA']
        'Washington, DC'
        >>> capitals['FRA']
        'Paris'
    """
    return extract_string_feature(
        return_government_data,
        extract_capital,
        'capital',
        verbose=verbose
    )


if __name__ == "__main__":
    # Test extraction
    capitals = get_capital(verbose=True)

    # Show sample results
    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'IND', 'AUS']:
        print(f"  {iso3}: {capitals.get(iso3, 'N/A')}")
