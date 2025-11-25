"""Extract country background/overview text."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.c_01_intoduction.return_introduction_data import return_introduction_data


def extract_background(parsed_data: Dict) -> str:
    """Extract background from parsed Introduction data."""
    return parsed_data.get('background', '')


def get_background(verbose: bool = False) -> Dict[str, str]:
    """
    Get background for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to background values

    Example:
        >>> data = get_background()
        >>> data['USA']
        'Britain's American colonies broke with the mother country in 1776...'
    """
    return extract_string_feature(
        return_introduction_data,
        extract_background,
        'background',
        verbose=verbose
    )


if __name__ == "__main__":
    data = get_background(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA']:
        val = data.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
