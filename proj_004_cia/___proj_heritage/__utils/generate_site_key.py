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
