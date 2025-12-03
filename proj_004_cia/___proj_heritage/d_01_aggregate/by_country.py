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


if __name__ == "__main__":
    """Test country aggregation with real data."""
    from proj_004_cia.___proj_heritage.a_01_load import load_heritage_data
    from proj_004_cia.___proj_heritage.c_01_normalize import normalize_all_sites

    print("=" * 70)
    print("AGGREGATE BY COUNTRY TEST")
    print("=" * 70)

    # Load and normalize
    print("\nLoading data...")
    sites = load_heritage_data()
    normalized = normalize_all_sites(sites)

    print(f"Aggregating {len(normalized)} sites by country...")
    by_country = aggregate_by_country(normalized)

    print(f"\n✓ Aggregated into {len(by_country)} countries")
    print("-" * 70)

    # Top 10 countries
    top_countries = sorted(by_country.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    print("\nTop 10 Countries by Site Count:")
    for i, (iso3, country_sites) in enumerate(top_countries, 1):
        country_name = country_sites[0]['geography']['countries'][iso3]['name']
        print(f"{i:2}. {country_name:30} ({iso3}): {len(country_sites):3} sites")

    # Sample country details
    sample_iso3 = top_countries[0][0]
    sample_sites = by_country[sample_iso3]
    sample_name = sample_sites[0]['geography']['countries'][sample_iso3]['name']

    print(f"\nSample Country: {sample_name} ({sample_iso3})")
    print("-" * 70)
    print(f"Total sites: {len(sample_sites)}")

    categories = {}
    for site in sample_sites:
        cat = site['classification']['category']['name']
        categories[cat] = categories.get(cat, 0) + 1

    print(f"\nBy Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:15} {count:3}")

    print(f"\nSample Sites (first 5):")
    for site in sample_sites[:5]:
        print(f"  - {site['names']['en']}")

    print("\n" + "=" * 70)
    print("✓ Country aggregation test completed!")
    print("=" * 70)
