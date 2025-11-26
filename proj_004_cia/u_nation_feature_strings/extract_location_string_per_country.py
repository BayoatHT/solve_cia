"""Extract geographic location description for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.c_02_geography.return_geography_data import return_geography_data


def extract_location(parsed_data: Dict) -> str:
    """
    Extract location description from parsed geography data.

    Handles both simple string locations and complex dict locations
    (for countries with multiple territories like France).
    """
    location = parsed_data.get('location', '')

    if isinstance(location, str):
        return location

    if isinstance(location, dict):
        # For countries with multiple territories (like France)
        # First check for 'description' key (general location)
        if 'description' in location:
            return location['description']

        # Otherwise, combine territory locations into a single string
        # Prioritize main/metropolitan territory if present
        parts = []
        priority_keys = ['metropolitan', 'main', 'description']
        other_parts = []

        for key, value in location.items():
            if isinstance(value, str) and value.strip():
                # Check if this is a priority key
                is_priority = any(pk in key.lower() for pk in priority_keys)
                if is_priority:
                    parts.insert(0, f"{key}: {value}")
                else:
                    other_parts.append(f"{key}: {value}")

        parts.extend(other_parts)
        return '; '.join(parts) if parts else ''

    return ''


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
