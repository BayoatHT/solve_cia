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
