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
