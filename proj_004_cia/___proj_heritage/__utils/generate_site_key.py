"""
Site key generation utilities.

Generates unique slugified keys from heritage site English names.
Handles collisions by appending country code or UNESCO ID.
"""

from typing import Dict, Set
from slugify import slugify


def generate_site_key(
    name_en: str,
    iso_codes: str = None,
    id_no: str = None,
    existing_keys: Set[str] = None
) -> str:
    """
    Generate unique site key from English name.

    Args:
        name_en: English name of the site
        iso_codes: ISO2 country codes (comma-separated), used for collision resolution
        id_no: UNESCO ID number, used as fallback for collision resolution
        existing_keys: Set of already generated keys to check for collisions

    Returns:
        Unique slugified site key

    Examples:
        >>> generate_site_key("Butrint")
        'butrint'

        >>> generate_site_key("Historic Centre of Prague")
        'historic_centre_of_prague'

        >>> generate_site_key("Al Qal'a of Beni Hammad")
        'al_qala_of_beni_hammad'

    Collision Handling:
        1. First attempt: slugify(name_en)
        2. If collision: append first ISO3 country code
        3. If still collision: append UNESCO ID number
    """
    if existing_keys is None:
        existing_keys = set()

    # Generate base key
    base_key = slugify(name_en, separator='_', lowercase=True)

    # Check if unique
    if base_key not in existing_keys:
        return base_key

    # Collision: try appending country code
    if iso_codes:
        from proj_004_cia.___proj_heritage.__config.iso_mapping import ISO2_TO_ISO3

        first_iso2 = iso_codes.split(',')[0].strip().upper()
        iso3 = ISO2_TO_ISO3.get(first_iso2)

        if iso3:
            key_with_country = f"{base_key}_{iso3.lower()}"
            if key_with_country not in existing_keys:
                return key_with_country

    # Still collision: append UNESCO ID
    if id_no:
        key_with_id = f"{base_key}_{id_no}"
        return key_with_id

    # Fallback: return base key (shouldn't happen with proper inputs)
    return base_key


def generate_all_site_keys(sites: list) -> Dict[str, str]:
    """
    Generate unique keys for all sites in dataset.

    Args:
        sites: List of site dictionaries with name_en, iso_codes, id_no

    Returns:
        Dictionary mapping UUID to site_key

    Example:
        >>> sites = [
        ...     {"uuid": "abc", "name_en": "Butrint", "iso_codes": "AL", "id_no": "570"},
        ...     {"uuid": "def", "name_en": "Louvre", "iso_codes": "FR", "id_no": "123"}
        ... ]
        >>> generate_all_site_keys(sites)
        {'abc': 'butrint', 'def': 'louvre'}
    """
    existing_keys = set()
    key_map = {}

    for site in sites:
        key = generate_site_key(
            name_en=site.get('name_en', ''),
            iso_codes=site.get('iso_codes'),
            id_no=site.get('id_no'),
            existing_keys=existing_keys
        )

        existing_keys.add(key)
        key_map[site['uuid']] = key

    return key_map


def validate_site_key(key: str) -> bool:
    """
    Validate that a site key is properly formatted.

    Args:
        key: Site key to validate

    Returns:
        True if valid, False otherwise

    Rules:
        - Lowercase letters, numbers, underscores only
        - No leading/trailing underscores
        - No consecutive underscores
        - Minimum 2 characters
    """
    if not key or len(key) < 2:
        return False

    # Check allowed characters
    if not all(c.islower() or c.isdigit() or c == '_' for c in key):
        return False

    # No leading/trailing underscores
    if key.startswith('_') or key.endswith('_'):
        return False

    # No consecutive underscores
    if '__' in key:
        return False

    return True


if __name__ == "__main__":
    """Test site key generation with real UNESCO data examples."""

    print("=" * 70)
    print("SITE KEY GENERATION UTILITIES TEST")
    print("=" * 70)

    # Test 1: Basic site key generation
    print("\n1. BASIC SITE KEY GENERATION")
    print("-" * 70)

    test_sites = [
        ("Butrint", "AL", "570", "Simple name"),
        ("Historic Centre of Prague", "CZ", "616", "Multi-word name"),
        ("Al Qal'a of Beni Hammad", "DZ", "102", "Special characters"),
        ("Alhambra, Generalife and Albayzín, Granada", "ES", "314", "Complex name"),
        ("18th-Century Royal Palace at Caserta", "IT", "549", "Starting with number"),
        ("Škocjan Caves", "SI", "390", "Unicode characters"),
    ]

    existing = set()
    for name, iso2, id_no, description in test_sites:
        key = generate_site_key(name, iso2, id_no, existing)
        existing.add(key)
        print(f"Site: {name}")
        print(f"  → Key: {key}")
        print(f"  → Valid: {validate_site_key(key)}")
        print(f"  → Note: {description}")
        print()

    # Test 2: Collision handling
    print("\n2. COLLISION HANDLING")
    print("-" * 70)

    existing_keys = set()

    # First site with name "Abbey"
    key1 = generate_site_key("Abbey of St Gall", "CH", "268", existing_keys)
    existing_keys.add(key1)
    print(f"First 'Abbey': {key1}")

    # Second site - different abbey
    key2 = generate_site_key("Abbey of Lorsch", "DE", "515", existing_keys)
    existing_keys.add(key2)
    print(f"Second 'Abbey': {key2}")

    # Simulate exact duplicate (would use country code)
    test_key = slugify("Abbey of St Gall", separator='_')
    existing_keys.add(test_key)
    key3 = generate_site_key("Abbey of St Gall", "FR", "999", existing_keys)
    print(f"Same name, different country: {key3}")
    print()

    # Test 3: Multiple sites batch processing
    print("\n3. BATCH KEY GENERATION")
    print("-" * 70)

    batch_sites = [
        {"uuid": "uuid-1", "name_en": "Acropolis, Athens", "iso_codes": "GR", "id_no": "404"},
        {"uuid": "uuid-2", "name_en": "Angkor", "iso_codes": "KH", "id_no": "668"},
        {"uuid": "uuid-3", "name_en": "Machu Picchu", "iso_codes": "PE", "id_no": "274"},
        {"uuid": "uuid-4", "name_en": "Petra", "iso_codes": "JO", "id_no": "326"},
        {"uuid": "uuid-5", "name_en": "Taj Mahal", "iso_codes": "IN", "id_no": "252"},
    ]

    key_map = generate_all_site_keys(batch_sites)

    print(f"Generated keys for {len(key_map)} sites:")
    for site in batch_sites:
        key = key_map[site['uuid']]
        print(f"  {site['name_en']:30} → {key}")
    print()

    # Test 4: Key validation
    print("\n4. KEY VALIDATION")
    print("-" * 70)

    validation_tests = [
        ("butrint", True, "Valid key"),
        ("historic_centre_of_prague", True, "Valid with underscores"),
        ("abbey_123", True, "Valid with numbers"),
        ("INVALID", False, "Uppercase not allowed"),
        ("_leading", False, "Leading underscore"),
        ("trailing_", False, "Trailing underscore"),
        ("double__underscore", False, "Consecutive underscores"),
        ("a", False, "Too short"),
        ("site-name", False, "Hyphen not allowed"),
        ("", False, "Empty string"),
    ]

    for key, expected, description in validation_tests:
        valid = validate_site_key(key)
        status = "✓" if valid == expected else "✗"
        print(f"{status} {repr(key):35} Valid: {valid:5} ({description})")

    # Test 5: Edge cases
    print("\n5. EDGE CASES")
    print("-" * 70)

    edge_cases = [
        ("São Paulo", "BR", "1000", "Portuguese characters"),
        ("Tīwānaku", "BO", "567", "Macrons"),
        ("Old City & Walls", "IL", "148", "Ampersand"),
        ("Site (North)", "NO", "200", "Parentheses"),
        ("1234 Numeric Site", "XX", "999", "Starting with numbers"),
    ]

    edge_existing = set()
    for name, iso2, id_no, description in edge_cases:
        key = generate_site_key(name, iso2, id_no, edge_existing)
        edge_existing.add(key)
        valid = validate_site_key(key)
        print(f"{name:30} → {key:35} (Valid: {valid})")
    print()

    # Summary
    print("=" * 70)
    print("✓ All site key generation tests completed!")
    print(f"✓ Generated {len(existing_keys) + len(edge_existing)} unique keys")
    print("=" * 70)
