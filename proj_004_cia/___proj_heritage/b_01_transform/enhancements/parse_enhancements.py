"""
Parse enhancements for public-facing data.

Adds:
- UNESCO official URLs
- External links structure
- Geographic context (continent, type)
- Historical context (decade, age)
- Metadata (source, license, attribution)
"""

from typing import Dict
from datetime import datetime


def parse_enhancements(site: Dict, normalized: Dict) -> Dict:
    """
    Add enhancements to normalized site data.

    Args:
        site: Raw site dictionary
        normalized: Normalized site dictionary

    Returns:
        Dictionary with enhancement data

    Example:
        >>> enhancements = parse_enhancements(raw_site, normalized_site)
        >>> enhancements['links']['unesco']
        'https://whc.unesco.org/en/list/570'
    """
    unesco_id = site.get('id_no', '')
    inscription_year = normalized['temporal']['inscription']['primary_date']

    return {
        'links': generate_links(unesco_id),
        'geographic_context': generate_geographic_context(normalized),
        'historical_context': generate_historical_context(inscription_year),
        'metadata': generate_metadata(),
        'search_text': generate_search_text(normalized),
    }


def generate_links(unesco_id: str) -> Dict:
    """
    Generate external links for the site.

    Args:
        unesco_id: UNESCO site ID

    Returns:
        Dictionary with external links
    """
    base_unesco_url = "https://whc.unesco.org/en/list"

    return {
        'unesco_official': f"{base_unesco_url}/{unesco_id}",
        'unesco_documents': f"{base_unesco_url}/{unesco_id}/documents",
        'unesco_gallery': f"{base_unesco_url}/{unesco_id}/gallery",
        'unesco_map': f"{base_unesco_url}/{unesco_id}/map",
        'wikipedia': None,  # To be populated externally
        'wikidata': None,   # To be populated externally
        'official_website': None,  # To be populated externally
    }


def generate_geographic_context(normalized: Dict) -> Dict:
    """
    Generate enhanced geographic context.

    Args:
        normalized: Normalized site data

    Returns:
        Dictionary with geographic context
    """
    region_code = normalized['geography']['region']['code']

    # Map regions to continents
    region_to_continent = {
        'EUR': 'Europe',
        'ASP': 'Asia',  # Asia and Pacific
        'LAC': 'Americas',  # Latin America and Caribbean
        'AFR': 'Africa',
        'ARB': 'Asia',  # Arab States (mostly Asia/Africa)
    }

    continent = region_to_continent.get(region_code, 'Unknown')

    # Determine geographic type from description
    geographic_type = infer_geographic_type(normalized)

    return {
        'continent': continent,
        'geographic_type': geographic_type,
        'has_coordinates': normalized['geography']['coordinates']['available'],
        'is_coastal': 'coastal' in geographic_type.lower() if geographic_type else False,
    }


def infer_geographic_type(normalized: Dict) -> str:
    """
    Infer geographic type from site data.

    Args:
        normalized: Normalized site data

    Returns:
        Geographic type string
    """
    description = normalized['descriptions']['short'].get('en', '').lower()
    category = normalized['classification']['category']['name']

    # Simple keyword-based inference
    if any(word in description for word in ['mountain', 'alpine', 'peak', 'highland']):
        return 'Mountain'
    elif any(word in description for word in ['coast', 'coastal', 'sea', 'ocean', 'island', 'beach']):
        return 'Coastal'
    elif any(word in description for word in ['desert', 'arid', 'sahara']):
        return 'Desert'
    elif any(word in description for word in ['forest', 'jungle', 'rainforest']):
        return 'Forest'
    elif any(word in description for word in ['city', 'urban', 'town', 'historic centre']):
        return 'Urban'
    elif any(word in description for word in ['river', 'valley', 'canyon']):
        return 'River/Valley'
    elif category == 'Natural':
        return 'Natural Landscape'
    else:
        return 'Cultural Landscape'


def generate_historical_context(inscription_year: int) -> Dict:
    """
    Generate historical context from inscription year.

    Args:
        inscription_year: Year site was inscribed

    Returns:
        Dictionary with historical context
    """
    if not inscription_year:
        return {
            'decade': None,
            'era': None,
            'age_years': None,
        }

    current_year = datetime.now().year
    age = current_year - inscription_year

    # Determine decade
    decade = f"{(inscription_year // 10) * 10}s"

    # Determine era
    if inscription_year < 1980:
        era = 'Early Heritage Period (1972-1979)'
    elif inscription_year < 1990:
        era = 'Expansion Period (1980-1989)'
    elif inscription_year < 2000:
        era = 'Growth Period (1990-1999)'
    elif inscription_year < 2010:
        era = 'Modern Period (2000-2009)'
    elif inscription_year < 2020:
        era = 'Contemporary Period (2010-2019)'
    else:
        era = 'Recent Period (2020+)'

    return {
        'decade': decade,
        'era': era,
        'age_years': age,
        'inscription_year': inscription_year,
    }


def generate_metadata() -> Dict:
    """
    Generate dataset metadata.

    Returns:
        Dictionary with metadata
    """
    return {
        'data_source': 'UNESCO World Heritage Centre',
        'data_provider': 'UNESCO',
        'license': 'UNESCO Copyright',
        'attribution': 'Data provided by UNESCO World Heritage Centre (whc.unesco.org)',
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'version': '2024',
    }


def generate_search_text(normalized: Dict) -> str:
    """
    Generate searchable full-text field.

    Args:
        normalized: Normalized site data

    Returns:
        Concatenated searchable text
    """
    texts = [
        normalized['names'].get('en', ''),
        normalized['descriptions']['short'].get('en', ''),
        normalized['descriptions'].get('full', ''),
        ' '.join(c['name'] for c in normalized['geography']['countries'].values()) if normalized['geography']['countries'] else '',
        normalized['geography']['region'].get('name', ''),
        normalized['classification']['category'].get('name', ''),
    ]

    # Concatenate and clean
    search_text = ' '.join(str(t) for t in texts if t)
    return ' '.join(search_text.split())  # Normalize whitespace


if __name__ == "__main__":
    """Test enhancements parser with normalized site data."""
    import json
    from pathlib import Path
    from proj_004_cia.___proj_heritage.c_01_normalize import normalize_all_sites
    from proj_004_cia.___proj_heritage.a_01_load import load_heritage_data

    print("=" * 70)
    print("ENHANCEMENTS PARSER TEST")
    print("=" * 70)

    # Load and normalize sample sites
    print("\nLoading and normalizing sample sites...")
    sites = load_heritage_data()[:5]  # First 5 sites
    normalized = normalize_all_sites(sites)

    print(f"Testing enhancements for {len(normalized)} sites:")
    print("-" * 70)

    for i, site in enumerate(normalized, 1):
        print(f"\n{i}. {site['names']['en']}")
        print("   " + "=" * 65)

        # Links
        print(f"   UNESCO URL: {site['links']['unesco_official']}")

        # Geographic context
        print(f"\n   Geographic Context:")
        print(f"     Continent: {site['geographic_context']['continent']}")
        print(f"     Type: {site['geographic_context']['geographic_type']}")

        # Historical context
        print(f"\n   Historical Context:")
        print(f"     Era: {site['historical_context']['era']}")
        print(f"     Age: {site['historical_context']['age_years']} years")

        # Metadata
        print(f"\n   Metadata:")
        print(f"     Source: {site['metadata']['data_source']}")
        print(f"     License: {site['metadata']['license']}")

        # Search text
        search_text = site['search_text'][:100]
        print(f"\n   Search text: {search_text}...")

    print("\n" + "=" * 70)
    print("✓ Enhancements parser test completed!")
    print("=" * 70)
