"""
Parse identity attributes: names, keys, and identifiers.
"""

from typing import Dict
from proj_004_cia.___proj_heritage.__utils.generate_site_key import generate_site_key
from proj_004_cia.___proj_heritage.__utils.clean_text import clean_text
from proj_004_cia.___proj_heritage.__config.config import LANGUAGES


def parse_identity(site: Dict, existing_keys: set = None) -> Dict:
    """
    Parse all identity-related attributes from raw site data.

    Args:
        site: Raw site dictionary
        existing_keys: Set of already-generated keys for collision detection

    Returns:
        Dictionary with identity data

    Example:
        >>> site = {"name_en": "Butrint", "uuid": "abc", "id_no": "570"}
        >>> parse_identity(site)
        {
            'site_key': 'butrint',
            'uuid': 'abc',
            'unesco_id': '570',
            'names': {'en': 'Butrint', ...}
        }
    """
    # Generate unique site key
    site_key = generate_site_key(
        name_en=site.get('name_en', ''),
        iso_codes=site.get('iso_codes'),
        id_no=site.get('id_no'),
        existing_keys=existing_keys
    )

    # Parse all language names
    names = {}
    for lang in LANGUAGES:
        name_field = f'name_{lang}'
        if name_field in site:
            names[lang] = clean_text(site[name_field])

    return {
        'site_key': site_key,
        'uuid': site.get('uuid'),
        'unesco_id': site.get('id_no'),
        'names': names
    }


if __name__ == "__main__":
    """Test identity parser with real heritage site data."""
    import json
    from pathlib import Path

    print("=" * 70)
    print("IDENTITY PARSER TEST")
    print("=" * 70)

    # Load sample sites
    data_file = Path(__file__).parents[2] / "_raw_data" / "json" / "all_world_heritage.json"
    with open(data_file) as f:
        sites = json.load(f)

    # Test with first 3 sites
    TEST_SITES = 3
    existing_keys = set()

    print(f"\nTesting with first {TEST_SITES} sites:")
    print("-" * 70)

    for i, site in enumerate(sites[:TEST_SITES], 1):
        print(f"\n{i}. SITE: {site.get('name_en', 'Unknown')}")
        print("   " + "=" * 65)

        result = parse_identity(site, existing_keys)

        print(f"   Key:        {result['site_key']}")
        print(f"   UUID:       {result['uuid']}")
        print(f"   UNESCO ID:  {result['unesco_id']}")

        print(f"\n   Names (6 languages):")
        for lang, name in result['names'].items():
            print(f"     {lang}: {name[:60]}{'...' if len(name) > 60 else ''}")

        existing_keys.add(result['site_key'])

    print("\n" + "=" * 70)
    print(f"✓ Identity parser test completed!")
    print(f"✓ Generated {len(existing_keys)} unique site keys")
    print("=" * 70)
