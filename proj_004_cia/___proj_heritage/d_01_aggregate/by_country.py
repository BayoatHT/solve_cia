"""
Aggregate sites by country (ISO3 codes).
"""

from typing import Dict, List
from collections import defaultdict
from proj_004_cia.__logger.logger import app_logger
from proj_004_cia.___proj_heritage.__config.iso_mapping import ISO3_TO_COUNTRY_NAME


def aggregate_by_country(normalized_sites: List[Dict]) -> Dict[str, Dict]:
    """
    Group sites by country (ISO3 code).

    Transboundary sites appear under each country they span.

    Args:
        normalized_sites: List of normalized site dictionaries

    Returns:
        Dictionary with country ISO3 codes as keys, country data as values

    Example:
        >>> sites = normalize_all_sites(raw_sites)
        >>> by_country = aggregate_by_country(sites)
        >>> by_country['FRA']['total_sites']
        52
    """
    app_logger.info("Aggregating sites by country...")

    country_data = defaultdict(lambda: {
        'country_code': None,
        'country_name': None,
        'total_sites': 0,
        'sites_by_category': {'Cultural': 0, 'Natural': 0, 'Mixed': 0},
        'transboundary_sites': 0,
        'endangered_sites': 0,
        'sites': []
    })

    # Group sites by country
    for site in normalized_sites:
        countries = site['geography']['countries']
        is_transboundary = site['geography']['is_transboundary']
        is_endangered = site['temporal']['danger_status']['is_endangered']
        category = site['classification']['category']['name']

        for iso3 in countries.keys():
            # Initialize country data if first site
            if country_data[iso3]['country_code'] is None:
                country_data[iso3]['country_code'] = iso3
                country_data[iso3]['country_name'] = ISO3_TO_COUNTRY_NAME.get(iso3, 'Unknown')

            # Add site to country
            country_data[iso3]['sites'].append(site['site_key'])
            country_data[iso3]['total_sites'] += 1

            # Update category counts
            country_data[iso3]['sites_by_category'][category] += 1

            # Update flags
            if is_transboundary:
                country_data[iso3]['transboundary_sites'] += 1

            if is_endangered:
                country_data[iso3]['endangered_sites'] += 1

    # Convert to regular dict and sort by site count
    result = dict(country_data)

    # Sort countries by site count (descending)
    result = dict(sorted(
        result.items(),
        key=lambda x: x[1]['total_sites'],
        reverse=True
    ))

    app_logger.success(f"✓ Aggregated {len(result)} countries")

    return result


def get_country_stats(country_data: Dict) -> Dict:
    """
    Get statistics about country aggregation.

    Args:
        country_data: Output from aggregate_by_country()

    Returns:
        Dictionary with statistics

    Example:
        >>> by_country = aggregate_by_country(sites)
        >>> stats = get_country_stats(by_country)
        >>> stats['total_countries']
        170
    """
    stats = {
        'total_countries': len(country_data),
        'countries_with_sites': len([c for c in country_data.values() if c['total_sites'] > 0]),
        'top_countries': [],
        'countries_with_most_sites': None,
        'average_sites_per_country': 0,
    }

    if country_data:
        # Top 10 countries by site count
        sorted_countries = sorted(
            country_data.items(),
            key=lambda x: x[1]['total_sites'],
            reverse=True
        )
        stats['top_countries'] = [
            {
                'code': code,
                'name': data['country_name'],
                'sites': data['total_sites']
            }
            for code, data in sorted_countries[:10]
        ]

        # Country with most sites
        top = sorted_countries[0]
        stats['countries_with_most_sites'] = {
            'code': top[0],
            'name': top[1]['country_name'],
            'sites': top[1]['total_sites']
        }

        # Average sites per country
        total_sites = sum(data['total_sites'] for data in country_data.values())
        stats['average_sites_per_country'] = round(total_sites / len(country_data), 2)

    return stats


def get_sites_for_country(country_data: Dict, iso3_code: str) -> List[str]:
    """
    Get list of site keys for a specific country.

    Args:
        country_data: Output from aggregate_by_country()
        iso3_code: ISO3 country code

    Returns:
        List of site keys

    Example:
        >>> by_country = aggregate_by_country(sites)
        >>> french_sites = get_sites_for_country(by_country, 'FRA')
    """
    if iso3_code in country_data:
        return country_data[iso3_code]['sites']
    return []
