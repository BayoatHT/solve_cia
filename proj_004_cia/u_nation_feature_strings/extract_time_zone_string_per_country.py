"""Extract time zone description for each country."""

from typing import Dict
from proj_004_cia.u_nation_feature_strings.base_extractor import extract_string_feature
from proj_004_cia.a_04_iso_to_cia_code.iso3Code_to_cia_code import load_country_data


def parse_time_zone(raw_data: Dict, iso3Code: str) -> Dict:
    """Parse time zone from raw data."""
    # Time zone info is in Government > Capital > time difference
    gov_section = raw_data.get('Government', {})
    capital_data = gov_section.get('Capital', {})

    time_diff = ''
    if isinstance(capital_data, dict):
        tz_data = capital_data.get('time difference', {})
        if isinstance(tz_data, dict):
            time_diff = tz_data.get('text', '').strip()

    return {
        'time_zone': time_diff
    }


def extract_time_zone(parsed_data: Dict) -> str:
    """Extract time zone from parsed data."""
    return parsed_data.get('time_zone', '')


def get_time_zone(verbose: bool = False) -> Dict[str, str]:
    """
    Get time zone description for all countries.

    Args:
        verbose: If True, print extraction statistics

    Returns:
        Dictionary mapping ISO3 codes to time zone descriptions

    Example:
        >>> zones = get_time_zone()
        >>> zones['USA']
        'UTC-5 (during Standard Time)'
    """
    return extract_string_feature(
        parse_time_zone,
        extract_time_zone,
        'time_zone',
        verbose=verbose
    )


if __name__ == "__main__":
    zones = get_time_zone(verbose=True)

    print("\nSample results:")
    for iso3 in ['USA', 'FRA', 'CHN', 'BRA', 'AUS']:
        val = zones.get(iso3, 'N/A')
        display = f"{val[:80]}..." if len(val) > 80 else val
        print(f"  {iso3}: {display}")
