"""
Parse geographic attributes: coordinates, countries, regions.
"""

from typing import Dict
from proj_004_cia.___proj_heritage.__utils.parse_coordinates import parse_coordinates
from proj_004_cia.___proj_heritage.__utils.handle_null_values import handle_missing_coordinates
from proj_004_cia.___proj_heritage.__config.iso_mapping import (
    parse_iso_codes_string,
    get_country_info
)


def parse_geographic(site: Dict) -> Dict:
    """
    Parse all geographic attributes from raw site data.

    Args:
        site: Raw site dictionary

    Returns:
        Dictionary with geographic data including coordinates, countries, region

    Example:
        >>> site = {
        ...     "coordinates": {"lat": 39.745732, "lon": 20.02095},
        ...     "iso_codes": "AL",
        ...     "states_names": ["Albania"],
        ...     "region": "Europe and North America",
        ...     "region_code": "EUR",
        ...     "transboundary": "False"
        ... }
        >>> parse_geographic(site)
        {
            'coordinates': {...},
            'countries': {'ALB': {...}},
            'region': {...},
            'is_transboundary': False
        }
    """
    # Parse coordinates
    coords = parse_coordinates(site.get('coordinates'))
    coord_data = handle_missing_coordinates(coords, site.get('name_en'))

    # Parse countries (ISO2 to ISO3 conversion)
    iso_codes_str = site.get('iso_codes', '')
    iso3_codes = parse_iso_codes_string(iso_codes_str)

    countries = {}
    for iso3 in iso3_codes:
        # Get country info using ISO3
        from proj_004_cia.___proj_heritage.__config.iso_mapping import ISO3_TO_ISO2, ISO3_TO_COUNTRY_NAME
        iso2 = ISO3_TO_ISO2.get(iso3)
        countries[iso3] = {
            'name': ISO3_TO_COUNTRY_NAME.get(iso3, 'Unknown'),
            'iso2': iso2,
            'iso3': iso3
        }

    # Parse region
    region = {
        'name': site.get('region'),
        'code': site.get('region_code')
    }

    # Transboundary status
    is_transboundary = site.get('transboundary') == 'True'

    return {
        'coordinates': coord_data,
        'countries': countries,
        'region': region,
        'is_transboundary': is_transboundary,
        'country_count': len(countries)
    }


if __name__ == "__main__":
    """Test geographic parser with real heritage site data."""
    import json
    from pathlib import Path

    print("=" * 70)
    print("GEOGRAPHIC PARSER TEST")
    print("=" * 70)

    # Load sample sites
    data_file = Path(__file__).parents[2] / "_raw_data" / "json" / "all_world_heritage.json"
    with open(data_file) as f:
        sites = json.load(f)

    # Test with diverse geographic examples
    TEST_SITES = 5

    print(f"\nTesting with first {TEST_SITES} sites:")
    print("-" * 70)

    for i, site in enumerate(sites[:TEST_SITES], 1):
        print(f"\n{i}. SITE: {site.get('name_en', 'Unknown')}")
        print("   " + "=" * 65)

        result = parse_geographic(site)

        print(f"   Region: {result['region']['name']} ({result['region']['code']})")

        if result['coordinates']['available']:
            coords = result['coordinates']
            print(f"   Coordinates: {coords['latitude']}, {coords['longitude']}")
        else:
            print(f"   Coordinates: Not available")

        print(f"\n   Countries ({len(result['countries'])}):")
        for iso3, country in result['countries'].items():
            print(f"     {iso3}: {country['name']}")

        print(f"\n   Transboundary: {result['transboundary']['is_transboundary']}")

    print("\n" + "=" * 70)
    print("✓ Geographic parser test completed!")
    print("=" * 70)
