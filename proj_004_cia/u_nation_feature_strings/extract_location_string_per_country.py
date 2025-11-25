"""Extract geographic location description for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data


def extract_location(parsed_data: Dict) -> str:
    """Extract location description from parsed geography data."""
    return parsed_data.get('location', '')


def get_location(verbose: bool = False) -> Dict[str, str]:
    """
    Get geographic location description for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to location descriptions

    Example:
        >>> locations = get_location()
        >>> locations['USA']
        'North America, bordering both the North Atlantic Ocean and the North Pacific Ocean, between Canada and Mexico'
    """
    return extract_string_feature(
        return_geography_data,
        extract_location,
        'location',
        verbose=verbose
    )


if __name__ == "__main__":
    locations = get_location(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'JPN', 'BRA', 'EGY']:
        loc = locations.get(iso3, 'N/A')
        print(f"  {iso3}: {loc[:80]}..." if len(loc) > 80 else f"  {iso3}: {loc}")
