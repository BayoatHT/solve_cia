"""
Parse temporal attributes: inscription dates and danger status.
"""

from typing import Dict
from proj_004_cia.___proj_heritage.__utils.parse_date import parse_inscription_dates


def parse_temporal(site: Dict) -> Dict:
    """
    Parse all temporal attributes from raw site data.

    Args:
        site: Raw site dictionary

    Returns:
        Dictionary with inscription dates and danger status

    Example:
        >>> site = {
        ...     "date_inscribed": "1992",
        ...     "secondary_dates": "1992, 1999",
        ...     "danger": "False",
        ...     "danger_list": None,
        ...     "date_end": None
        ... }
        >>> parse_temporal(site)
        {
            'inscription': {...},
            'danger_status': {...}
        }
    """
    # Parse inscription dates
    inscription = parse_inscription_dates(
        date_inscribed=site.get('date_inscribed', ''),
        secondary_dates=site.get('secondary_dates')
    )

    # Parse danger status
    is_endangered = site.get('danger') == 'True'
    danger_status = {
        'is_endangered': is_endangered,
        'details': site.get('danger_list') if is_endangered else None,
        'date_end': site.get('date_end')
    }

    return {
        'inscription': inscription,
        'danger_status': danger_status
    }
