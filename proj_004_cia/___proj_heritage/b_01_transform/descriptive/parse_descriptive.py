"""
Parse descriptive attributes: descriptions and justifications.
"""

from typing import Dict
from proj_004_cia.___proj_heritage.__utils.clean_text import clean_text
from proj_004_cia.___proj_heritage.__config.config import LANGUAGES


def parse_descriptive(site: Dict) -> Dict:
    """
    Parse all descriptive attributes from raw site data.

    Args:
        site: Raw site dictionary

    Returns:
        Dictionary with descriptions in all languages and justification

    Example:
        >>> site = {
        ...     "short_description_en": "Ancient site...",
        ...     "short_description_fr": "Site ancien...",
        ...     "description_en": "Full description...",
        ...     "justification_en": "UNESCO justification..."
        ... }
        >>> parse_descriptive(site)
        {
            'short_descriptions': {'en': '...', 'fr': '...'},
            'full_description': '...',
            'justification': '...'
        }
    """
    # Parse short descriptions (all languages)
    short_descriptions = {}
    for lang in LANGUAGES:
        field = f'short_description_{lang}'
        if field in site:
            short_descriptions[lang] = clean_text(site[field])

    # Parse full description (English only)
    full_description = clean_text(site.get('description_en', ''))

    # Parse justification (English only)
    justification = clean_text(site.get('justification_en', ''))

    return {
        'short_descriptions': short_descriptions,
        'full_description': full_description,
        'justification': justification
    }
